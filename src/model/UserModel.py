class User:
    def __init__(self, username=None, posts=None, following=None, followers=None, profile_picture=None):
        self.username = username
        self.posts = posts
        self.following = following
        self.followers = followers
        self.profile_picture = profile_picture
        self.followers_list = []
        self.following_list = []

    def addProfilePicture(self, profile_picture):
        self.profile_picture = profile_picture

    def addHeader(self, posts, following, followers):
        self.posts = posts
        self.following = following
        self.followers = followers

    def addFollowers(self, user):
        self.followers_list.append(user)

    def addFollowing(self, user):
        if user not in self.following:
            self.following_list.append(user)