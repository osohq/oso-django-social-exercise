allow(user, "list", "Post") if
    user.is_staff;

allow(user: social::User, "create", post: social::Post) if
    user.in_group(post.group);

allow(user: social::User, "list_posts", group: django::contrib::auth::Group) if
    user.in_group(group);
