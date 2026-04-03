# This file is responsible for configuring ImageKit client

from imagekitio  import ImageKit
from app.core.config import settings
import imagekitio
print(imagekitio.__file__)

imagekit = ImageKit(
    # public_key=settings.IMAGEKIT_PUBLIC_KEY,
    private_key=settings.IMAGEKIT_PRIVATE_KEY,
    # url_endpoint=settings.IMAGEKIT_URL_ENDPOINT
)


