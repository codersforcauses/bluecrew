from PIL import Image, ExifTags
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from ..models import TileInteraction, BingoGrid
from ..models import User
from io import BytesIO


class ImageExifRemovalTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")

        # Create test image
        image = Image.new("RGB", (100, 100), color="red")
        buffer = BytesIO()

        exif = image.getexif()
        gps_ifd = {}

        # Set dummy GPS latitude and longitude EXIF metadata
        gps_ifd[1] = 'S'
        gps_ifd[2] = ((19, 1), (45, 1), (519948, 10000))
        gps_ifd[3] = 'E'
        gps_ifd[4] = ((149, 1), (14, 1), (392059, 10000))

        gps_tag = ExifTags.GPSTAGS.get('GPSInfo', None)

        if gps_tag is not None:
            exif[gps_tag] = gps_ifd

        image.save(buffer, format="JPEG", exif=exif)
        buffer.seek(0)
        self.image = SimpleUploadedFile("test_image_with_exif.jpg", buffer.read(), content_type="image/jpeg")

    def test_exif_metadata_removed(self):
        """Test that EXIF metadata is removed after image processing with django-resized."""
        # Check EXIF metadata exists before attempting to remove
        img_data = BytesIO(self.image.read())
        img = Image.open(img_data)
        exif_before = img._getexif()

        self.assertIsNotNone(exif_before)

        grid = BingoGrid.objects.create(is_active=True)

        tile = TileInteraction.objects.create(
            user=self.user,
            position=1,
            grid=grid,
            image=self.image,
            consent=True,
            completed=False
        )

        image_path = tile.image.path
        with open(image_path, "rb") as img_file:
            img_data = img_file.read()

        img = Image.open(BytesIO(img_data))
        exif_after = img._getexif()

        self.assertIsNone(exif_after)
