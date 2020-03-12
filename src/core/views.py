import json
import typing as t
from json import JSONDecodeError
from http import HTTPStatus

from flask import request as global_request, Response, abort
from flask.views import View
from werkzeug import Request
from werkzeug.exceptions import HTTPException

from core.db import Base, session
from core.models import BaseModel
from core.serialization.exceptions import ValidationError
from core.serialization.schemas import Schema


class DetailObjectMixin:
    model_class: t.Type[BaseModel] = None
    url_param: str = None

    def raise_not_found_response(self) -> Response:
        raise abort(404)

    def get_object(self, row_id: int) -> t.Type[BaseModel]:
        return session.query(self.model_class).get(row_id)

    def _get_object_or_404(self, **kw):
        obj = self.get_object(kw.get(self.url_param))

        if not obj:
            return self.raise_not_found_response()

        return obj


class ApiView(View):
    schema_class: t.Type[Schema] = None

    @property
    def request(self) -> Request:
        return global_request

    def get_handler_or_raise_405(self) -> t.Callable:
        handler = getattr(self, self.request.method.lower(), None)

        if not handler:
            raise abort(Response(
                response=json.dumps({
                    'code': 'method_not_allowed',
                    'message': 'Method is not allowed',
                }),
                content_type='application/json',
                status=HTTPStatus.METHOD_NOT_ALLOWED.value,
            ))

        return handler

    def dispatch_request(self, *args, **kw) -> Response:
        handler = self.get_handler_or_raise_405()

        try:
            response = handler(*args, **kw)
        except JSONDecodeError as e:
            return Response(
                response=json.dumps({
                    'code': 'internal_error',
                    'message': str(e),
                }),
                content_type='application/json',
                status=HTTPStatus.BAD_REQUEST.value,
            )
        except ValidationError as e:
            return Response(
                response=json.dumps({'errors': e.details}),
                status=HTTPStatus.BAD_REQUEST.value,
                content_type='application/json',
            )
        except HTTPException as e:
            raise e
        except Exception:
            import traceback
            traceback.print_exc()

            return Response(
                response=json.dumps({
                    'code': 'internal_error',
                    'message': 'Internal error.',
                }),
                content_type='application/json',
                status=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )

        return response

    def get_schema(self) -> Schema:
        return self.schema_class()


class ListApiView(ApiView):
    model_class: t.Type[Base] = None
    order_by_param: str= 'order_by'

    def get_objects(self) -> t.List[t.Type[BaseModel]]:
        order_by_field = self.request.args.get('order_by')

        if order_by_field:
            model_field = getattr(self.model_class, order_by_field.replace('-', ''))
            model_field_with_order = (
                model_field.desc()
                if order_by_field.startswith('-')
                else model_field.asc()
            )
            return session.query(self.model_class).order_by(model_field_with_order)

        return session.query(self.model_class).all()

    def get(self) -> Response:
        filtered_objects = self.get_objects()
        objects_as_dict = [f.asdict() for f in filtered_objects]
        serialized_objects = self.get_schema().serialize_many(objects_as_dict)

        return Response(
            response=json.dumps(serialized_objects),
            status=HTTPStatus.OK.value,
            content_type='application/json',
        )


class DetailApiView(DetailObjectMixin, ApiView):
    def get(self, **kw) -> Response:
        obj = self._get_object_or_404(**kw)

        return Response(
            response=json.dumps(self.get_schema().serialize(obj.asdict())),
            status=HTTPStatus.OK.value,
            content_type='application/json',
        )


class CreateApiView(ApiView):
    model_class = None

    def deserialize(self, data: dict) -> dict:
        return self.get_schema().deserialize(data)

    def serialize(self, data: dict) -> dict:
        return self.get_schema().serialize(data)

    def pre_serialize(self, serialized_data: dict) -> dict:
        return serialized_data

    def post(self) -> Response:
        try:
            request_data = self.request.json
            deserialized_object = self.deserialize(request_data)
            model = self.init_model(deserialized_object)
            created_object = self.create(model)
        except ValidationError as e:
            return Response(
                response=json.dumps({'errors': e.details}),
                status=HTTPStatus.BAD_REQUEST.value,
                content_type='application/json',
            )

        serialized_object = self.serialize(created_object.asdict())

        return Response(
            response=json.dumps(serialized_object),
            status=HTTPStatus.CREATED.value,
            content_type='application/json',
        )

    def init_model(self, deserialized_object: dict) -> t.Type[BaseModel]:
        return self.model_class(**deserialized_object)

    def create(self, model: t.Type[BaseModel]) -> t.Type[BaseModel]:
        session.add(model)
        session.commit()
        return model


class UpdateApiView(DetailObjectMixin, ApiView):
    def deserialize(
            self,
            data: t.Mapping[str, t.Any],
            partial: bool = False
    ) -> t.Mapping[str, t.Any]:
        return self.get_schema().deserialize(data=data, partial=partial)

    def serialize(self, data: t.Mapping[str, t.Any]) -> t.Mapping[str, t.Any]:
        return self.get_schema().serialize(data)

    def post_serialize(self, serialized_data: t.Mapping[str, t.Any]) -> t.Mapping[str, t.Any]:
        return serialized_data

    def update(self, obj, data: t.Mapping[str, t.Any]) -> t.Type[BaseModel]:
        for k, v in data.items():
            setattr(obj, k, v)

        session.commit()

        return obj

    def put(self, partial: bool = False, **kw) -> Response:
        obj = self._get_object_or_404(**kw)

        try:
            request_data = self.request.json
            deserialized_object = self.deserialize(data=request_data, partial=partial)
            updated_object = self.update(obj, deserialized_object)
        except ValidationError as e:
            return Response(
                response=json.dumps({'errors': e.details}),
                status=HTTPStatus.BAD_REQUEST.value,
                content_type='application/json',
            )

        serialized_object = self.serialize(updated_object.asdict())
        serialized_object = self.post_serialize(serialized_object)

        return Response(
            response=json.dumps(serialized_object),
            status=HTTPStatus.OK.value,
            content_type='application/json',
        )


class PatchApiView(UpdateApiView):
    def patch(self, **kw) -> Response:
        return self.put(partial=True, **kw)


class ActionApiView(ApiView):
    def deserialize(self, data):
        return self.get_schema().deserialize(data)

    def serialize(self, data):
        return self.get_schema().serialize(data)

    def post(self):
        try:
            request_data = self.request.json
            deserialized_object = self.deserialize(request_data)
        except ValidationError as e:
            return Response(
                response=json.dumps({'errors': e.details}),
                status=HTTPStatus.BAD_REQUEST.value,
                content_type='application/json',
            )

        action_result = self.make_action(deserialized_object)

        return Response(
            response=json.dumps(action_result),
            status=HTTPStatus.CREATED.value,
            content_type='application/json',
        )

    def make_action(self, deserialized_data):
        return deserialized_data


class DestroyApiView(DetailObjectMixin, ApiView):
    def destroy(self, obj) -> None:
        session.delete(obj)

    def delete(self, **kw) -> Response:
        obj = self._get_object_or_404(**kw)
        self.destroy(obj)

        return Response(
            response=json.dumps({}),
            status=HTTPStatus.NO_CONTENT.value,
            content_type='application/json',
        )
