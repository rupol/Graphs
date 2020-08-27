import random


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        # maps IDs to User objects (lookup table for User Objects given IDs)
        self.users = {}
        # Adjacency list
        # maps user_ids to a list of other users (who are their friends)
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for i in range(0, num_users):
            self.add_user(f"User {i+1}")  # name doesn't really matter

        # Create friendships
        # generate all possible friendships
        # avoid duplicate friendships
        possible_friendships = []
        for user_id in self.users:
            # if friendship between user 1 and user 2 already exists
            # don't add friendship between user 2 and user 1
            # to prevent this, only look at friendships for user ids higher than user
            friend_id = user_id + 1
            while friend_id < self.last_id + 1:
                possible_friendships.append((user_id, friend_id))
                friend_id += 1

        # randomly selected X friendships
        # X = num_users * avg_friendships // 2, so we don't count each friendship twice since they are bidirectional
        random.shuffle(possible_friendships)
        num_friendships = num_users * avg_friendships // 2
        for i in range(0, num_friendships):
            user_1, user_2 = possible_friendships[i]
            self.add_friendship(user_1, user_2)

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        # store the friend ID (key): path from user -> friend (value, as a list of user IDs)
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        # traverse the shortest path between user and all other connected users (BFS)

        queue = [[user_id]]
        while queue:
            current_path = queue.pop(0)
            current_user = current_path[-1]

            if current_user not in visited:
                # save friend_ID: [shortest path from user_id -> friend_id] in visited
                visited[current_user] = current_path

                for next_friend in self.friendships[current_user]:
                    new_path = list(current_path)
                    new_path.append(next_friend)
                    queue.append(new_path)
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    num_users = 2000
    average_friendships = 5
    sg.populate_graph(num_users, average_friendships)
    # print(sg.friendships)
    user_id = 1
    connections = sg.get_all_social_paths(user_id)
    print(
        f"Percentage of users in user {user_id}'s social network = {(len(connections)/num_users)*100}%")
    total = 0
    for path in connections.values():
        total += len(path)
    print(f"Avg degree of separation = {total / len(connections) - 1}")
