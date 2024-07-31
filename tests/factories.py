from faker import Faker
from factory.django import DjangoModelFactory, Password
from factory import SubFactory, LazyFunction, LazyAttributeSequence, lazy_attribute, post_generation

from accounts.models import User
from articles.models import Article

fake = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    first_name = LazyFunction(fake.first_name)
    last_name = LazyFunction(fake.last_name)
    email = LazyAttributeSequence(
        lambda obj, count: '%s@example.com' % (f'{obj.first_name}.{obj.last_name}{str(count)}')
    )
    password = Password('veryStrongP@$$123')
    date_of_birth = LazyFunction(fake.date_this_century)

    @lazy_attribute
    def role(self):
        return User.SUBSCRIBER
    
    @post_generation
    def admin(self, create, extracted, **kwargs):
        if extracted:
            self.role = User.ADMIN
            self.is_staff = True
            self.is_superuser = True
    
    @post_generation
    def author(self, create, extracted, **kwargs):
        if extracted:
            self.role = User.AUTHOR

    
class ArticleFactory(DjangoModelFactory):
    class Meta:
        model = Article

    title = LazyFunction(fake.word)
    description = LazyFunction(fake.word)
    content = LazyFunction(fake.word)
    author = SubFactory(UserFactory)

    @lazy_attribute
    def visibility(self):
        return Article.PUBLIC
    
    @post_generation
    def private(self, create, extracted, **kwargs):
        if extracted:
            self.visibility = Article.PRIVATE
