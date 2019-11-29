from flask import (
    make_response,
    abort,
)
from config import db
from model import (
    User,
    UserSchema,
)

def read_all():
    """
    This function responds to a request for /api/user
    with the complete lists of user

    :return:        json string of list of user
    """
    # Create the list of user from our data
    user = User.query \
        .order_by(User.ctime) \
        .all()

    # Serialize the data for the response
    user_schema = UserSchema(many=True)
    #return user_schema.dump(user).data
    return user_schema.dump(user)

def read_one(id):
    """
    This function responds to a request for /api/user/{user_id}
    with one matching person from user

    :param user_id:     ID of user to find
    :return:            user matching ID
    """
    # Get the person requested
    user = User.query \
        .filter(User.id == id) \
        .one_or_none()

    # Did we find a user?
    if user is not None:

        # Serialize the data for the response
        user_schema = UserSchema()
        #return user_schema.dump(user).data
        return user_schema.dump(user)

    # Otherwise, nope, didn't find that person
    else:
        abort(404, 'User not found for Id: {id}'.format(id=id))

def create(user):
    """
    This function creates a new user in the user structure
    based on the passed-in user data

    :param user:  user to create in user structure
    :return:        201 on success, 406 on user exists
    """
    uid = user.get('uid')
    fullname = user.get('fullname')

    existing_user = User.query \
        .filter(User.uid == uid) \
        .one_or_none()

    # Can we insert this user?
    if existing_user is None:

        # Create a user instance using the schema and the passed-in user
        schema = UserSchema()
        new_user = schema.load(user, session=db.session).data

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Serialize and return the newly created user in the response
        return schema.dump(new_user).data, 201

    # Otherwise, nope, user exists already
    else:
        abort(409, f'User {fullname} exists already')

def update(user_id, user):
    """
    This function updates an existing person in the people structure
    Throws an error if a person with the name we want to update to
    already exists in the database.
    :param person_id:   Id of the person to update in the people structure
    :param person:      person to update
    :return:            updated person structure
    """
    # Get the person requested from the db into session
    update_user = User.query.filter(
        User.user_id == user_id
    ).one_or_none()

    # Try to find an existing person with the same name as the update
    uid = user.get("uid")

    existing_user = (
        User.query.filter(User.uid == uid)
        .one_or_none()
    )

    # Are we trying to find a person that does not exist?
    if update_user is None:
        abort(
            404,
            "User not found for Id: {uid}".format(user_id=id),
        )

    # Would our update create a duplicate of another person already existing?
    elif (
        existing_user is not None and existing_user.uid != uid
    ):
        abort(
            409,
            "Person {fullname} exists already".format(
                fullname=fullname
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in person into a db object
        schema = UserSchema()
        update = schema.load(user, session=db.session).data

        # Set the id to the person we want to update
        update.uid = update_user.uid

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated person in the response
        data = schema.dump(update_person).data

        return data, 200

def delete(user_id):
    """
    This function deletes a person from the people structure
    :param person_id:   Id of the person to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the person requested
    user = User.query.filter(User.id == user_id).one_or_none()

    # Did we find a person?
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return make_response(
            "User {user_id} deleted".format(user_id=user_id), 200
        )

    # Otherwise, nope, didn't find that person
    else:
        abort(
            404,
            "User not found for Id: {user_id}".format(user_id=user_id),
        )