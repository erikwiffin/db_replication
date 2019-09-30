# pylint: disable=no-member
from db_replication.extensions import db
from db_replication.models.relational.post import Post

follows = db.Table(
    "follows",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("followee_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)

posts = db.Table(
    "posts",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    following = db.relationship(
        "User",
        secondary=follows,
        primaryjoin=id == follows.c.follower_id,
        secondaryjoin=id == follows.c.followee_id,
        lazy=True,
    )

    posts = db.relationship(
        "Post",
        secondary=posts,
        lazy=True,
    )

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.following = []
        self.posts = []

    def follow(self, user):
        self.following.append(user)

    def write_post(self, title, body):
        self.posts.append(Post(title, body))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username
