from http import HTTPStatus

from django.http import HttpResponse


class HTMX:
    @staticmethod
    def redirect(url: str) -> HttpResponse:
        return HttpResponse(url, status=HTTPStatus.OK, headers={"HX-Location": url})
