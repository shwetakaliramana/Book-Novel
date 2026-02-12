from django.core.management.base import BaseCommand
from adminapp.models import Author, Category, Era, Brand, Book

class Command(BaseCommand):
    help = 'Populate database with sample book data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting sample data creation...'))

        # Create Categories
        categories = ['Romance', 'Mystery', 'Science Fiction', 'Fantasy', 'Historical Fiction']
        category_objects = {}
        for cat_name in categories:
            cat, created = Category.objects.get_or_create(name=cat_name)
            category_objects[cat_name] = cat
            status = "Created" if created else "Already exists"
            self.stdout.write(f"  ✓ {status}: {cat_name}")

        # Create Authors
        authors = ['Jane Austen', 'Agatha Christie', 'Isaac Asimov', 'J.K. Rowling', 'George R.R. Martin']
        author_objects = {}
        for author_name in authors:
            author, created = Author.objects.get_or_create(name=author_name)
            author_objects[author_name] = author
            status = "Created" if created else "Already exists"
            self.stdout.write(f"  ✓ {status}: {author_name}")

        # Create Eras
        eras = ['Regency Era', 'Victorian Era', 'Modern Era', 'Contemporary']
        era_objects = {}
        for era_name in eras:
            era, created = Era.objects.get_or_create(name=era_name)
            era_objects[era_name] = era
            status = "Created" if created else "Already exists"
            self.stdout.write(f"  ✓ {status}: {era_name}")

        # Create Brand
        brand, created = Brand.objects.get_or_create(name="Penguin Classics")
        status = "Created" if created else "Already exists"
        self.stdout.write(f"  ✓ {status}: Penguin Classics")

        # Create Sample Books
        books_data = [
            {
                "title": "Pride and Prejudice",
                "author": "Jane Austen",
                "category": "Romance",
                "era": "Regency Era",
                "description": "A romantic novel of manners and marriage among the British gentry. Elizabeth Bennet navigates social expectations while finding love.",
                "status": "featured",
                "stock": 10
            },
            {
                "title": "Murder on the Orient Express",
                "author": "Agatha Christie",
                "category": "Mystery",
                "era": "Modern Era",
                "description": "A famous detective must solve a murder on a luxury train with a cast of suspicious passengers.",
                "status": "featured",
                "stock": 8
            },
            {
                "title": "Foundation",
                "author": "Isaac Asimov",
                "category": "Science Fiction",
                "era": "Modern Era",
                "description": "An epic science fiction series about the fall and rise of civilization using psychohistory.",
                "status": "featured",
                "stock": 6
            },
            {
                "title": "Harry Potter and the Sorcerer's Stone",
                "author": "J.K. Rowling",
                "category": "Fantasy",
                "era": "Contemporary",
                "description": "A young wizard discovers his magical heritage and attends Hogwarts School of Witchcraft and Wizardry.",
                "status": "trending",
                "stock": 15
            },
            {
                "title": "Emma",
                "author": "Jane Austen",
                "category": "Romance",
                "era": "Regency Era",
                "description": "A witty novel about a young woman who meddles in others' romantic affairs while avoiding her own.",
                "status": "trending",
                "stock": 7
            },
            {
                "title": "The Murder of Roger Ackroyd",
                "author": "Agatha Christie",
                "category": "Mystery",
                "era": "Modern Era",
                "description": "A detective investigates the murder of a wealthy businessman with shocking twists.",
                "status": "normal",
                "stock": 5
            },
            {
                "title": "I, Robot",
                "author": "Isaac Asimov",
                "category": "Science Fiction",
                "era": "Modern Era",
                "description": "A collection of short stories about robots and artificial intelligence exploring the three laws of robotics.",
                "status": "trending",
                "stock": 9
            },
            {
                "title": "Harry Potter and the Chamber of Secrets",
                "author": "J.K. Rowling",
                "category": "Fantasy",
                "era": "Contemporary",
                "description": "Harry's second year at Hogwarts brings new mysteries and dangerous magical creatures.",
                "status": "normal",
                "stock": 12
            },
            {
                "title": "Sense and Sensibility",
                "author": "Jane Austen",
                "category": "Romance",
                "era": "Regency Era",
                "description": "Two sisters with contrasting personalities navigate love, marriage, and social expectations.",
                "status": "normal",
                "stock": 8
            },
            {
                "title": "Death on the Nile",
                "author": "Agatha Christie",
                "category": "Mystery",
                "era": "Modern Era",
                "description": "A honeymoon cruise becomes a murder mystery when a wealthy heiress is killed.",
                "status": "trending",
                "stock": 6
            },
        ]

        self.stdout.write(self.style.SUCCESS('\nCreating books...'))
        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                title=book_data["title"],
                defaults={
                    "author": author_objects[book_data["author"]],
                    "category": category_objects[book_data["category"]],
                    "era": era_objects[book_data["era"]],
                    "brand": brand,
                    "description": book_data["description"],
                    "status": book_data["status"],
                    "stock": book_data["stock"],
                }
            )
            status = "Created" if created else "Already exists"
            self.stdout.write(f"  ✓ {status}: {book.title}")

        self.stdout.write(self.style.SUCCESS('\n✓ Sample data created successfully!'))