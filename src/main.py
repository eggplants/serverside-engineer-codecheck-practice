import collections
import csv
import sys

PlayDataMostCommonList = list[tuple[str, int]]
PlayDataRankedList = list[tuple[int, str, int]]


def read_csv(filepath: str) -> PlayDataMostCommonList:
    data: dict[str, list[int]] = {}
    with open(filepath) as f:
        rows = csv.DictReader(f)
        for row in rows:
            player_id = row["player_id"]
            score = int(row["score"])
            if player_id in data:
                data[player_id].append(score)
            else:
                data[player_id] = [score]

    return sorted(
        collections.Counter(
            {
                player_id: round(sum(scores) / len(scores))
                for player_id, scores in data.items()
            }
        ).most_common(),
        key=lambda x: (
            -x[1],
            x[0],
        ),
    )


def create_csv_content(lst: PlayDataMostCommonList, n: int = 10) -> PlayDataRankedList:
    rows: PlayDataRankedList = []

    prev_score = -float("inf")
    rank_num = 0
    same_count = 1

    for player_id, score in lst:
        if prev_score == score:
            rows.append(
                (
                    rank_num,
                    player_id,
                    score,
                )
            )
            same_count += 1
        else:
            if len(rows) + 1 > n:
                break
            rank_num += same_count
            rows.append(
                (
                    rank_num,
                    player_id,
                    score,
                )
            )
            same_count = 1
        prev_score = score

    return rows


def main() -> int:
    filename = sys.argv[1]

    lst = read_csv(filename)
    print("rank,player_id,mean_score")
    rows = create_csv_content(lst)
    for rank, player_id, score in rows:
        print(rank, player_id, score, sep=",")

    return 0


if __name__ == "__main__":
    sys.exit(main())
