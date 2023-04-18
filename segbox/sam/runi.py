import uvicorn
from my_model import predict
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route


def index(request):
    return PlainTextResponse("My Index Page!")


def model_stats(request):
    return JSONResponse({'stats': [1, 0, 2, 3]})


def model_predict(request):
    prediction_req = request.json()

    prediction = predict(prediction_req)

    return JSONResponse(prediction)


routes = [Route('/', index), Route('/stats', model_stats), Route('/predict', model_predict, methods=['POST'])]


app = Starlette(debug=True, routes=routes)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
