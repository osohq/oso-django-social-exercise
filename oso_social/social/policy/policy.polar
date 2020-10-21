allow(user, "read", _: social::Post) if
    user.is_staff;

allow(user, "read", post: social::Post) if
    (post.group = user.groups.values_list("id") or post.group = None) and post.access_level = social::Post.ACCESS_PUBLIC;

allow(user: social::User, "read", post: social::Post) if
    post.access_level = social::Post.ACCESS_PRIVATE and post.created_by = user;

allow(user: social::User, "create", post: social::Post) if
    user.in_group(post.group);

allow(user: social::User, "list_posts", group: django::contrib::auth::Group) if
    user.in_group(group);
