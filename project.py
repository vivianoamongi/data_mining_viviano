import pandas as pd

# Load the dataset
try:
    df = pd.read_csv('cwurData.csv')
except FileNotFoundError:
    print("Error: The file 'cwurData.csv' was not found.")
    exit()

# Filter for the most recent year to get a current ranking
df_2015 = df[df['year'] == 2015].sort_values(by='score', ascending=False)
df_2015.reset_index(drop=True, inplace=True)

# A dictionary to group universities by country and store their scores
university_data = {}
for index, row in df_2015.iterrows():
    country = row['country']
    if country not in university_data:
        university_data[country] = []
    university_data[country].append({'name': row['institution'], 'score': row['score'], 'rank': index + 1})

class University:
    """A class to represent a university and track its ranking progress."""
    def __init__(self, name, country, score, rank):
        self.name = name
        self.country = country
        self.score = score
        self.rank = rank
        self.ranking_history = [{'year': 2015, 'score': score, 'rank': rank}]

    def update_ranking(self, year, new_score):
        """Updates the university's score and recalculates its rank."""
        self.score = new_score
        
        # This is a simplification; in a real-world scenario, you would
        # re-rank the entire list of universities to get the new rank.
        # For this exercise, we will assume a rank change for demonstration.
        
        # A simple check to simulate rank change based on score
        if new_score > self.ranking_history[0]['score']:
            new_rank = self.rank - 1
            print(f"Great news! {self.name} improved its score. Its new rank is likely higher.")
        elif new_score < self.ranking_history[0]['score']:
            new_rank = self.rank + 1
            print(f"Oops! {self.name}'s score dropped. Its new rank is likely lower.")
        else:
            new_rank = self.rank
        
        self.rank = new_rank
        self.ranking_history.append({'year': year, 'score': new_score, 'rank': new_rank})
        print(f"Ranking data for {self.name} updated for {year}.")

    def show_progress(self):
        """Displays the progress of the university based on its ranking history."""
        if len(self.ranking_history) > 1:
            initial = self.ranking_history[0]
            current = self.ranking_history[-1]
            score_change = current['score'] - initial['score']
            rank_change = initial['rank'] - current['rank']

            print(f"\n--- Progress for {self.name} ({self.country}) ---")
            print(f"Initial Rank ({initial['year']}): #{initial['rank']} | Score: {initial['score']:.2f}")
            print(f"Current Rank ({current['year']}): #{current['rank']} | Score: {current['score']:.2f}")

            if rank_change > 0:
                print(f"Rank change: ↑ {rank_change} positions (Improvement)")
            elif rank_change < 0:
                print(f"Rank change: ↓ {abs(rank_change)} positions (Decline)")
            else:
                print("Rank change: → No change in rank")
        else:
            print(f"No progress to show for {self.name} yet.")

def create_university_objects(data):
    """
    Function to create a list of University objects from the grouped data.
    Uses loops to iterate through the dictionary and create objects.
    """
    all_universities = []
    for country, universities in data.items():
        for uni in universities:
            all_universities.append(University(uni['name'], country, uni['score'], uni['rank']))
    return all_universities

def rank_and_display(universities):
    """
    Function to sort and display the top universities by their current score.
    Uses a list and a loop to present the data.
    """
    universities.sort(key=lambda x: x.score, reverse=True)
    
    print("\n*** Top 10 World University Ranking (2015 Data) ***")
    for i in range(10): # Using a loop to show only the top 10
        uni = universities[i]
        print(f"#{uni.rank}: {uni.name} ({uni.country}) - Score: {uni.score:.2f}")

# Main execution
if __name__ == "__main__":
    
    # Use the first function to create the list of University objects
    university_objects = create_university_objects(university_data)
    
    # Use the second function to display the initial ranking
    rank_and_display(university_objects)
    
    # Demonstrate the class methods with a specific university
    # We will pick a few to show progress
    oxford = None
    yale = None
    
    for uni in university_objects:
        if uni.name == 'University of Oxford':
            oxford = uni
        if uni.name == 'Yale University':
            yale = uni
            
    # Simulate a score change for Oxford and show its progress
    if oxford:
        print("\n--- Simulating an update for University of Oxford ---")
        oxford.update_ranking(2016, 85.0) # Assume a better score
        oxford.show_progress()
    
    # Simulate a score change for Yale and show its progress
    if yale:
        print("\n--- Simulating an update for Yale University ---")
        yale.update_ranking(2016, 78.5) # Assume a slightly lower score
        yale.show_progress()