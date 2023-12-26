
from models import db, User, Post, PostTag, Tag
from app import app

db.drop_all()
db.create_all()

ahmed = User(first_name="Ahmed",
             last_name="Hennawy")
noor = User(first_name="Noor",
            last_name="Al-Jamea")
manar = User(first_name="Manar",
             last_name="Al-Jamea")

db.session.add_all([ahmed, noor, manar])
db.session.commit()
post_ah1 = Post(title="hi, ahmed", content="My first post", user_id=1)
post_no1 = Post(title="hi, noor", content="My first post", user_id=2)
post_ma1 = Post(title="hi, manar", content="My first post", user_id=3)

db.session.add_all([post_ah1, post_no1, post_ma1])
db.session.commit()


cat_tag = Tag(name="cat")
dog_tag = Tag(name="dog")
tiger_tag = Tag(name="tiger")

db.session.add_all([cat_tag, dog_tag, tiger_tag])

db.session.commit()

post_tag1_ah = PostTag(post_id=1, tag_id=1)
post_tag2_ah = PostTag(post_id=1, tag_id=2)
post_tag1_no = PostTag(post_id=2, tag_id=2)
post_tag2_no = PostTag(post_id=2, tag_id=3)
post_tag1_ma = PostTag(post_id=3, tag_id=3)
post_tag2_ma = PostTag(post_id=3, tag_id=1)

db.session.add_all([post_tag1_ah, post_tag2_ah,
                   post_tag1_no, post_tag2_no,
                   post_tag1_ma, post_tag2_ma])
db.session.commit()
