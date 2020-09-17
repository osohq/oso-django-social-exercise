# Allow anyone to view any public posts.
allow(_actor, "view", post: social::Post) if
    post.access_level = social::Post.ACCESS_PUBLIC;

# Allow a user to view their private posts.
allow(actor: social::User, "view", post: social::Post) if
    post.access_level = social::Post.ACCESS_PRIVATE and
    post.created_by = actor;

# allow(actor: social::User, "view", post: social::Post) if
#     post.contents.find(actor.tag) >= 0;

# allow(actor: social::User { username: "admin" }, "view", post: social::Post);
