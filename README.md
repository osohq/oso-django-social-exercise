# oso - oso Django Social Exercise

In this workshop, we will add authorization to a Django social web app.  First, we will enforce authorization using Python & Django.  Then, we will incorporate the `django-oso` authorization library.

# Setup

Let's get setup.  Before we get started, we'll need a version of Python 3 and git.  If you don't have Python 3 yet, we'd recommend installing with [pyenv](https://github.com/pyenv/pyenv), which lets you easily switch versions.

There are a few steps to get our app up and running before we can work on it:

1. Clone the repo from: [https://github.com/osohq/oso-django-social-exercise](https://github.com/osohq/oso-django-social-exercise)

    `git clone git@github.com:osohq/oso-django-social-exercise.git`

2. Make sure your current environment is using python 3 (`python —-version`).  Some folks might need to use the `python3` command depending on your system.
3. Change directory into the cloned project: `cd oso-django-social-exercise`
4. Create a virtual environment to isolate the dependencies we are about to install: `python -m venv venv`
5. Activate the virtual environement: `. venv/bin/activate`
6. Install `pip install -r requirements.txt`
7. Enter the `oso_social` directory: `cd oso_social`
8. Run migrations: `./manage.py migrate`
9. Create static files: `./manage.py collectstatic`
10. Load fixture data: `./manage.py loaddata social-oso.yaml`
11. Run site: `./manage.py runserver`
12. The site should now be accessible at http://localhost:8000.  There is no authorization yet.  Poke around, and create some posts.  There are existing users called:
    - dhatch
    - bowler
    - user
    - superuser_admin

    The login system doesn't validate passwords, so just login with whatever account you'd like to test.  You can create a new account by entering a new username.

## Project Structure

The app is a Django project.  In our top level directory, we have a `README`.  The project code is located in the `oso_social` directory.  This directory contains the `social` directory, and the `./manage.py` command which we will use throughout for running tests and the server.

**All paths below are relative to the `oso_social` directory.** Make sure you `cd` into that for the rest of the workshop.

## Running tests

To make it easier to follow along, we've added tests that correspond to each step. These tests are located in `social/tests.py`.

Each step has an associated test that can be run to check that the step is complete.  To start off, let's run the test for Step 0 (making sure we are ready and our setup is working).

```bash
$ ./manage.py test social.tests.Step0
```

 

Some tests will start to fail as we continue to make authorization more restricted throughout the workshop, so make sure to always run the test for the right step!

# **1. Limiting posts to admins**

Our current application has no authorization.  First, we'll add a simple authorization rule to the Post Feed (http://localhost:8000).

Start in the `social/views.py` file.  This file contains Django view functions that handle requests to our app:

- `list_posts` Retrieves all posts from the database and returns them.
- `new_post` Handles post creation by rendering a form and handling submissions.

The routing of requests is handled with a [Django URLConf](https://docs.djangoproject.com/en/3.1/topics/http/urls/) in `social/urls.py`.

At the end of each view function, we use the `render` function, which takes a Django template and renders it with a particular set of context variables.

Let's add a simple rule to this page: **Only admins can view posts.** **Non-admin users retrieve an empty list of posts.**

*Tip:* We've added a comment where our new code should go.  Each subsequent step has associated comments where new code should be added.

*Changes*

- Add some logic to the `list_posts` view function to return an empty list of posts if the user is not an admin.
- If the user is an admin, all posts should be returned.
- Make sure the page still returns successfully for unauthorized users, but does not include any posts.

*Hint*

Use the `is_staff` property on `request.user` to determine if the logged in user is an admin.

*Testing*

To test this change, we can use the `superuser_admin` user.  This user is an administrator.  `bowler` is a non-admin user.

The admin status of a user can be modified in the admin interface at http://localhost:8000/admin.

Run `./manage.py test social.test.Step1` to run the automated tests.

# **2. Adding groups**

Groups are a common authorization scheme.  Typically, they restrict users from interacting with a particular part of an application based on what group they are in.  Users can be in one, or multiple groups.

We already have some functionality for groups in our app that is currently unused:

- The Post model in `social/models.py` has a `group` field that references the built in Django authentication `Group` model.
- The list template (`social/templates/social/list.html`) accepts two template variables:
    - `groups` a list of all groups, used to render links to each
    - `group` the current group, used to add a header with the group name.

In this step, we will allow users to submit posts to a particular group.  A user can only view a group's posts if they are a member of that group.

*Changes*

- Create a new view to list posts for a particular group.  The view function should be called `list_group`. The captured group argument from the URL above will be passed as a keyword argument to the function (the function argument's name must be `group_id`).
- In this view, render the list template with Posts filtered to contain only posts for the current group.
- In our `list_group` function, add logic to return an empty list of posts if the user is not a member of the group.

*Hints*

- Use QuerySet filtering to limit Posts to the correct group. [https://docs.djangoproject.com/en/3.1/ref/models/querysets/#filter](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#filter)
- The User model has a `in_group` function that may be helpful.

*Testing*

To test this change, we can use the `bowler` user. The `bowler` user is a member of the Bowling Club group (surprise!).  When logged in as this user, we should be able to view posts for the Bowling Club, but not the Django Meetup group.

Run `./manage.py test social.test.Step2` to run the automated tests.

# **3. Users can only create posts in groups they are a member of**

Ok, so far we've done half of what we set out to do.  Users can still write messages to groups they aren't a member of.  We don't want our `bowler` user to try to recruit folks from the Django Meetup to his bowling team.

Let's restrict Post creation in a similar way.  The `new_post` view function handles saving a new post.  The form is parsed with the call `form.save(commit=False)` into a Post model.  This model is saved to the database with the call to `post.save()`.

*Changes*

- We need to prevent a user from creating a post if they aren't a member of the group that the post is for.
- In this case, it's okay to return a not authorized response. We can do this by raising a `PermissionDenied` exception.
- Make sure that posts with no group are still allowed for any user!  We'll use these later.

*Hint*

This logic should be similar to the logic you used in the last step.

*Testing*

Try to post to the Django Meetup group as the `bowler` user.

Run the automated tests with: `./manage.py test social.test.Step3`.

# Discussion **& oso introduction**

Great! We just added groups & admin permissions to our app.

Now, we'll take a brief break and introduce you to oso.  In the rest of the workshop, we'll focus on how we can structure our authorization consistently using oso.

- In the next steps, we'll add oso to the app and use it for authorization.
- We'll do a few pieces together, then move on to some extensions & experiments.

*Hint*

If you're ahead, get started reading some our our docs:

- [Quickstart](https://docs.osohq.com/getting-started/quickstart.html)
- [Python Library Guide](https://docs.osohq.com/using/libraries/python/index.html)
- [Syntax Guide](https://docs.osohq.com/using/polar-syntax.html)
- [Policy Examples](https://docs.osohq.com/using/examples/index.html)

# **4. Use oso to authorize listing posts**

Now that we've introduced oso, let's start using it in our application.  We will update the authorization in `list_posts` to use oso.

To perform authorization with oso, we must:

1. Write our authorization policy
2. Enforce authorization by querying the policy for an authorization decision.

This app already has the [django-oso](https://docs.osohq.com/using/frameworks/django.html) authorization library installed.

*Changes*

- Create a new policy file in `social/policy/policy.polar`. You may need to create the `social/policy` directory.  `django-oso` will automatically load any policies in an installed app's `policy` directory.  Leave the policy empty for now.
- Now, let's enforce authorization.  The `django_oso.auth.authorize` function is the primary entrypoint to query the policy for an authorization decision.
    - `authorize` receives the following arguments: `authorize(request, resource, *, actor=None, action=None)`
    - Every authorization decision in oso is made over an `actor`, `action` and `resource`.
        - The `actor` is who is making the request.
        - The `action` is what the `actor` will do to `resource` if authorized.
        - The `resource` is what the request is performed on.
- In our `list_posts` view function, call `authorize` in place of our existing authorization logic.  Let's use the following values for `action` and `resource`:
    - `action`: `"list"`
    - `resource`: `"Post"`
- `django_oso` uses the logged in user as the `actor` by default.
- `authorize` will raise a `PermissionDenied` exception if authorization is denied.  Make sure to catch this in a `try / except` block to set the post list to empty.

- Now that we've added enforcement, let's test the list endpoint.  oso is deny by default and our policy is empty, so the admin user won't be able to see any posts.

- Let's add a new rule to our policy in `social/policy/policy.polar`:

    ```python
    allow(user, "list", "Post") if
    	user.is_staff;
    ```

    In oso, rules have a name and arguments.  The top level rule is `allow` and accepts an `actor`, `action`, and `resource`.  Arguments can either be a variable (`user`) in this case, or a literal value to match `"list"` and `"Post"`.

    This rule will allow a request if the user is staff (the same rule we had in our app previously).

*Testing*

- Check that `superuser_admin` can view posts, but other users cannot.

Run the automated test: `./manage.py test social.test.Step4`

# **5. Use oso to authorize listing groups & creating posts.**

Now, let's use oso for our other two authorization points.  In both cases, we will use the `authorize` function to query our policy & add a rule to the policy to handle authorization.

*Changes*

- Add `authorize` to `list_group`.
- Add a rule to the Polar policy that checks that the user is a member of the group.
    - **Hint**: This rule can use the `User.in_group` method.  Polar policies can call methods on objects that we pass into `authorize`.
- Add `authorize` to `new_post`.  This rule should be very similar to above.

*Hints*

- Sometimes, you may want to write a rule that only matches a particular type.  We can use *type specializers* to achieve this.  In the rule definition, use the `argument: type` syntax.  For example, the rule `allow(user, "view", post: social::Post)` would only match an `authorize` call where the `resource` is a `Post` model.
    - oso registers our app's models as specializers.
    - Some specializers you may want to use are:
        - User: `social::User`
        - Post: `social::Post`
        - Group `django::contrib::auth::Group`.

*Testing*

- The app should continue working as before after these changes.

Run `./manage.py test social.test.Step5` to run the tests.

# 6. Use oso to authorize each post

If you want to skip this step and just jump straight to experimenting, check out the `step6` tag: `git checkout step6`.

So far, the rules we've written authorize posts as a list.  For example:

- allow a user to list all posts on the feed view
- allow a user to list all posts for this group

But, we really want to get more specific.  A better feed view would show the user all posts for groups that they are in.  We also have a public & private field on posts.  It might include a user's own private posts and public posts that are not in a group.

To accomplish this with oso, we will query the policy for an authorization decision on each post.  

To do this, we will change our `authorize` call in `list_posts`:

```python
# in list_posts ...
authorized_posts = []
for post in posts:
    try:
        authorize(request, action="read", resource=post)
        authorized_posts.append(post)
    except PermissionDenied:
        continue

posts = authorized_posts
```

This method of enforcing authorization is fine for this example app and keeps things simple. But, it isn't very efficient.  In a real application, we'd need to push these filters down to the database to avoid fetching all posts and authorizing them one by one.  Later, we'll walk through a feature that is available as a preview in our current release to enable this or check out this [blog post](https://www.osohq.com/post/django-list-view) if you're ahead.

To use this new read action in our policy, we can write rules like below:

```python
allow(user: social::User, "read", post: social::Post) if
    user.in_group(post.group) and post.access_level = social::Post.ACCESS_PUBLIC;
```

This rule enables a user to read a post if they are a member of the post's group and the post is public.

*Changes*

- Use the code above in `list_posts`
- Call `authorize` for `list_group` in a similar structure.
- Update our policy as described above.  You will also need to write a new rule for admins to read all posts.
- Now, add a new rule that allows a user to read private posts created by the current user.

*Testing*

The feed view should now show all posts the user can see.  This includes a user's own private posts, a public post that is not made to a group, and public posts made in groups that the user is a member of.

We can test this with the `bowler` user, who should be able to see posts in the Bowling Club group.

Run test for step 6: `./manage.py test social.test.Step6`

# Experiment and Extensions

Now that we have oso installed in our app, let's experiment with adding some new features.  Below are some ideas, but feel free to come up with your own:

- Add friends to the app.
- Public and private groups
- Group admins
- User can read a post if they are `@mentioned` in it.
- Friends only posts.
- Only show groups the user is a member of on the home page and in the new post form.
- Add moderators that need to approve posts in groups before they are visible.

To help you along, our documentation may be helpful, in particular the below pages:

- [Quickstart](https://docs.osohq.com/getting-started/quickstart.html)
- [Python Library Guide](https://docs.osohq.com/using/libraries/python/index.html)
- [Syntax Guide](https://docs.osohq.com/using/polar-syntax.html)
- [Policy Examples](https://docs.osohq.com/using/examples/index.html)
