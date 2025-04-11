
IMAGE_NAME = ml_service_image
IMAGE_TAG = 1
CONTAINER_NAME = ml_service_container
SERVICE_PATH = services/ml_service
MODELS_PATH = services/models

build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) $(SERVICE_PATH)

run:
	docker run -d --rm \
	--name $(CONTAINER_NAME) \
	-p 8000:8000 \
	-v $(shell pwd)/$(MODELS_PATH):/models \
	$(IMAGE_NAME):$(IMAGE_TAG)

stop:
	docker stop $(CONTAINER_NAME)

rebuild: stop build run
