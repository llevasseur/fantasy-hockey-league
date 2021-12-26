import json 

ROSTERS_URL = "https://github.com/rylancole/world-juniors/blob/master/ROSTERS.md"
STANDINGS_URL = "https://github.com/rylancole/world-juniors/blob/master/STANDINGS.md"

def main():
  with open('../json/standings.json', 'r') as json_file:
    ranking_data = json.loads(json_file.read())

  standings = {}

  for user in ranking_data:
    scores = ranking_data[user]
    for category in scores:
      score = scores[category]
      if score != '-':
        if category in standings.keys():
          standings[category].append((score, user))
        else:
          standings[category] = [(score, user)]

  STANDINGS_md = open('../STANDINGS.md', 'w')

  overall_points = {}

  for category in standings:
    st = standings[category]
    st.sort()
    if category != "Goals Against Average": st.reverse()

    STANDINGS_md.write(f"## {category}\n")
    STANDINGS_md.write(f"| Rank | User | {category} |\n")
    STANDINGS_md.write(f"| :--- | ---- | ---------: |\n")

    last_p0 = st[0][0]
    i = 1
    j = 0
    for p in st:
      if p[0] != last_p0:
        i += j
        j = 1
      else:
        j += 1
      STANDINGS_md.write(f"| {i} | [{p[1]}]({ROSTERS_URL}#{p[1]}) |  {p[0]} |\n")
      last_p0 = p[0]

      if p[1] in overall_points.keys():
        overall_points[p[1]].append(7-i)
      else:
        overall_points[p[1]] = [7-i]

  README_md = open('../README.md', 'w')

  README_md.write(f"| User | [G]({STANDINGS_URL}#goals) | [A]({STANDINGS_URL}#assists) | SOG | [PIM]({STANDINGS_URL}#penalties-in-minutes) | [+/-]({STANDINGS_URL}#plus--minus) | TPM | [S%]({STANDINGS_URL}#save-percentage) | [GAA]({STANDINGS_URL}#goals-against-average) | Total |\n")
  README_md.write(f"| :--- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |  -----: |\n")

  for user in overall_points:
    README_md.write(f"| [{user}]({ROSTERS_URL}#{user}) | ")
    for p in overall_points[user]:
      README_md.write(f"{p} | ")
    README_md.write(f"{sum(overall_points[user])} |\n")

  

if __name__ == "__main__":
  main()