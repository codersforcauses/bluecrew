from django.test import TestCase
from ..models import User, Challenge, TileInteraction, BingoGrid
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.conf import settings
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
import shutil

TEST_DIR = 'test_data'


@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class ChallengeCompleteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
        )

        self.grid = BingoGrid.objects.create(is_active=True)
        self.challenges = []
        for i in range(16):
            c = Challenge.objects.create(
                name=f"Challenge {i}",
                description=f"Description {i}",
                challenge_type="act",
                points=5
            )
            self.challenges.append(c)
        self.grid.challenges.add(*self.challenges)

        self.tiles = []
        for i in range(16):
            t = TileInteraction.objects.create(
                user=self.user,
                grid=self.grid,
                position=i,
                completed=False
            )
            self.tiles.append(t)

        self.url = reverse("complete_challenge")

        # Create test image
        img = Image.new("RGB", (100, 100), color="red")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        self.image = SimpleUploadedFile("test_image.png", buffer.read(), content_type="image/png")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_already_completed_challenge(self):
        tile = self.tiles[0]
        tile.completed = True
        completion_date = timezone.now()
        tile.date_completed = completion_date
        tile.save()

        data = {
            "position": 0,
            "consent": True,
            "image": self.image
        }
        response = self.client.patch(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(self.tiles[0].date_completed, completion_date)

    def test_invalid_tile_position(self):
        data = {
            "position": 16,
            "consent": True,
            "image": self.image
        }
        response = self.client.patch(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_row_bingo(self):
        # complete all but last tile of first row
        for i in range(3):
            self.tiles[i].completed = True
            self.tiles[i].save()

        data = {
            "position": 3,
            "consent": False,
            "image": self.image
        }
        response = self.client.patch(self.url, data, format="multipart")

        tile = self.tiles[3]
        tile.refresh_from_db()
        self.image_path = tile.image.path

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["challenge_points"], self.challenges[data["position"]].points)
        self.assertEqual(response.data["bingo_row"], 0)
        self.assertEqual(response.data["bingo_col"], -1)
        self.assertEqual(response.data["bingo_diag"], -1)
        self.assertFalse(response.data["full_bingo"])
        self.assertEqual(
            response.data["bingo_points"], settings.BINGO_COMPLETE)

    def test_col_bingo(self):
        # complete all but last tile of second column
        for i in range(1, 10, 4):
            self.tiles[i].completed = True
            self.tiles[i].save()

        data = {
            "position": 13,
            "consent": False,
            "image": self.image
        }
        response = self.client.patch(self.url, data, format="multipart")

        tile = self.tiles[13]
        tile.refresh_from_db()
        self.image_path = tile.image.path

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["challenge_points"], self.challenges[data["position"]].points)
        self.assertEqual(response.data["bingo_row"], -1)
        self.assertEqual(response.data["bingo_col"], 1)
        self.assertEqual(response.data["bingo_diag"], -1)
        self.assertFalse(response.data["full_bingo"])
        self.assertEqual(
            response.data["bingo_points"], settings.BINGO_COMPLETE)

    def test_diag_complete(self):
        # complete bottom left to top right diagonal
        for i in range(3, 10, 3):
            self.tiles[i].completed = True
            self.tiles[i].save()

        data = {
            "position": 12,
            "consent": False,
            "image": self.image
        }
        response = self.client.patch(self.url, data, format="multipart")

        tile = self.tiles[12]
        tile.refresh_from_db()
        self.image_path = tile.image.path

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["challenge_points"], self.challenges[data["position"]].points)
        self.assertEqual(response.data["bingo_row"], -1)
        self.assertEqual(response.data["bingo_col"], -1)
        self.assertEqual(response.data["bingo_diag"], 3)
        self.assertFalse(response.data["full_bingo"])
        self.assertEqual(
            response.data["bingo_points"], settings.BINGO_COMPLETE)

    def test_grid_complete(self):
        # complete all but last tile of gird
        for i in range(15):
            self.tiles[i].completed = True
            self.tiles[i].save()

        data = {
            "position": 15,
            "consent": False,
            "image": self.image
        }
        response = self.client.patch(self.url, data, format="multipart")

        tile = self.tiles[15]
        tile.refresh_from_db()
        self.image_path = tile.image.path

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["challenge_points"], self.challenges[data["position"]].points)
        self.assertEqual(response.data["bingo_row"], 3)
        self.assertEqual(response.data["bingo_col"], 3)
        self.assertEqual(response.data["bingo_diag"], 0)
        self.assertTrue(response.data["full_bingo"])
        self.assertEqual(
            response.data["bingo_points"], settings.BINGO_COMPLETE*3 + settings.GRID_COMPLETE)

    def test_row_col_double_bingo(self):
        # Test a tile that completes both a row and a column

        # Complete position 4, 5, 7, i.e the second row
        for i in [4, 5, 7]:
            self.tiles[i].completed = True
            self.tiles[i].save()

        # Complete position 2, 10, 14, i.e. the third column
        for i in [2, 10, 14]:
            self.tiles[i].completed = True
            self.tiles[i].save()

        # This tile will complete both the row and the column
        data = {
            "position": 6,
            "consent": False,
            "image": self.image
        }
        response = self.client.patch(self.url, data, format="multipart")

        tile = self.tiles[6]
        tile.refresh_from_db()
        self.image_path = tile.image.path

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["challenge_points"], self.challenges[data["position"]].points)
        self.assertEqual(response.data["bingo_row"], 1)
        self.assertEqual(response.data["bingo_col"], 2)
        self.assertEqual(response.data["bingo_diag"], -1)
        self.assertFalse(response.data["full_bingo"])
        self.assertEqual(
            response.data["bingo_points"], 2*settings.BINGO_COMPLETE)

    def test_triple_bingo(self):
        # Test a tile that completes both a row, a column, and a diagonal

        # Complete position 4, 5, 7, i.e the second row
        for i in [4, 5, 7]:
            self.tiles[i].completed = True
            self.tiles[i].save()

        # Complete position 2, 10, 14, i.e. the third column
        for i in [2, 10, 14]:
            self.tiles[i].completed = True
            self.tiles[i].save()

        # Complete position 3, 9, 12, the second diagonal
        for i in [3, 9, 12]:
            self.tiles[i].completed = True
            self.tiles[i].save()

        # This tile will complete both the row, column, and diagonal
        data = {
            "position": 6,
            "consent": False,
            "image": self.image
        }
        response = self.client.patch(self.url, data, format="multipart")

        tile = self.tiles[6]
        tile.refresh_from_db()
        self.image_path = tile.image.path

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["challenge_points"], self.challenges[data["position"]].points)
        self.assertEqual(response.data["bingo_row"], 1)
        self.assertEqual(response.data["bingo_col"], 2)
        self.assertEqual(response.data["bingo_diag"], 3)
        self.assertFalse(response.data["full_bingo"])
        self.assertEqual(
            response.data["bingo_points"], 3*settings.BINGO_COMPLETE)

    def test_consent_patch(self):
        data = {
            "position": 6,
            "consent": True,
            "image": self.image
        }
        response = self.client.patch(self.url, data, format="multipart")

        tile = self.tiles[6]
        tile.refresh_from_db()
        self.image_path = tile.image.path

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tiles[6].refresh_from_db()
        self.assertTrue(self.tiles[6].consent)

    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass
