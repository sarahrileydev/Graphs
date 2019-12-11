import random


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
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
        Takes a number of users (nodes) and an average number of friendships (edges)
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
        for i in range(num_users):
            self.add_user(f"User: {i+1}")

        # Create friendships
        possible_friendships = []
        # Create a list with all possible friendship combinations

        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))

        # shuffle the list
        random.shuffle(possible_friendships)
        
        # print(possible_friendships)

        # then grab the first N elements from the list
        # Number of times to call add_friendships

        total_friendships = avg_friendships * num_users // 2
        # print(f"Friendships to create: {total_friendships}\n")
        for i in range(total_friendships):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])

    def get_all_social_paths(self, user_id):
        """
        BFT - because it says return EVERY user with SHORTEST path

        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        # BFT - for each connected friend, check to see if friend already in visited
        # if not create a key: [value] pair in visited

        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME

        # Create an empty queue and enqueue the starting [path]
        q = Queue()
        q.enqueue([user_id])

        # While the queue is not empty...
        while q.size() > 0:
            # Dequeue the first path
            path = q.dequeue()
            # If the last friend in the path has not been visited...
            last_friend = path[-1]
            if last_friend not in visited:
                # Mark it as visited
                visited[last_friend] = path
                # Then add all of it's neighbors to the back of the queue
                neighbors = self.friendships[last_friend]
                for neighbor in neighbors:
                    copy = path.copy()
                    copy.append(neighbor)
                    q.enqueue(copy)
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
