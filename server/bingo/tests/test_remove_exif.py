from PIL import Image, ExifTags
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from ..models import TileInteraction, BingoGrid, Challenge
from ..models import User
from io import BytesIO
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import override_settings
import shutil

TEST_DIR = 'test_data'


@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class ImageExifRemovalTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")

        self.grid = BingoGrid.objects.create(is_active=True)

        c = Challenge.objects.create(
                name="Challenge 1",
                description="Description 1",
                challenge_type="act",
                points=5
            )
        self.grid.challenges.add(c)

        self.tile = TileInteraction.objects.create(
            user=self.user,
            position=0,
            grid=self.grid,
            completed=False
        )

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

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.url = reverse('complete_challenge')

    def test_exif_removed(self):
        data = {
            "position": 0,
            "consent": True,
            "image": self.image
        }
        response = self.client.patch(self.url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.tile.refresh_from_db()
        img_data = self.tile.image.read()

        img = Image.open(BytesIO(img_data))
        exif_after = img._getexif()

        self.assertIsNone(exif_after)

    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass
