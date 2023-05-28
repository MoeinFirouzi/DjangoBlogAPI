from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User, Author
from blog.models import Post


class Command(BaseCommand):
    help = "Onserting dummy data"

    def __init__(self, *args, **kwarg):
        super(Command, self).__init__(*args, **kwarg)
        self.fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument(
            "-n",
            "--number",
            nargs=1,
            type=int,
            dest="number",
            required=True,
            metavar="number",
        )

    def handle(self, *args, **options):
        user = User.objects.create_user(
            email=self.fake.email(), password="test@12321",
            username=self.fake.name()
        )
        author = Author.objects.create(user=user, company=self.fake.company())

        n = options.get("number")[0]
        for i in range(n):
            Post.objects.create(
                author=author,
                title=self.fake.sentence(3),
                content=self.fake.paragraph(nb_sentences=5),
            )
