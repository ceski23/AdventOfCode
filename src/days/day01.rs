#[derive(Debug)]
enum Move {
    Left(i32),
    Right(i32),
}

fn parse_input(text: String) -> Option<Vec<Move>> {
    let moves = text
        .lines()
        .filter_map(|line| {
            let mut iter = line.chars();

            match (iter.next()?, iter.as_str().parse::<i32>().ok()?) {
                ('L', value) => Some(Move::Left(value)),
                ('R', value) => Some(Move::Right(value)),
                _ => None,
            }
        })
        .collect();

    Some(moves)
}

fn count_when_points_at_zero(moves: Vec<Move>, start_position: i32) -> i32 {
    let (_, count) = moves
        .iter()
        .fold((start_position, 0), |(position, count), next_move| {
            let non_normalized_position = match next_move {
                Move::Left(steps) => position - steps,
                Move::Right(steps) => position + steps,
            };
            let next_position = non_normalized_position.rem_euclid(100);

            (
                next_position,
                if next_position == 0 { count + 1 } else { count },
            )
        });

    count
}

fn count_when_passes_zero(moves: Vec<Move>, start_position: i32) -> i32 {
    let (_, count) = moves
        .iter()
        .fold((start_position, 0), |(position, count), next_move| {
            let non_normalized_position = match next_move {
                Move::Left(steps) => position - steps,
                Move::Right(steps) => position + steps,
            };
            let next_position = non_normalized_position.rem_euclid(100);
            // How many full 100-steps were taken (negative means moving left past 0)
            let wraps = non_normalized_position.div_euclid(100);
            // Adjust wrap count to count passes through 0 correctly
            let zero_count = match (position == 0, next_position == 0, wraps) {
                // Starting at 0 and moving left past it: don't count the starting point
                (true, _, wraps) if wraps < 0 => wraps.abs() - 1,
                // Landing exactly on 0 while moving left or not moving forward: include the landing
                (_, true, wraps) if wraps <= 0 => wraps.abs() + 1,
                // Otherwise just the absolute number of wraps
                _ => wraps.abs(),
            };

            (next_position, count + zero_count)
        });

    count
}

#[cfg(test)]
mod tests {
    use super::*;
    use anyhow::anyhow;
    use anyhow::Result;
    use std::fs;

    #[test]
    fn part1_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day01_test.txt")?;
        let data = parse_input(input).ok_or(anyhow!("Invalid input"))?;
        assert_eq!(count_when_points_at_zero(data, 50), 3);

        Ok(())
    }

    #[test]
    fn part1() -> Result<()> {
        let input = fs::read_to_string("inputs/day01.txt")?;
        let data = parse_input(input).ok_or(anyhow!("Invalid input"))?;
        assert_eq!(count_when_points_at_zero(data, 50), 1092);

        Ok(())
    }

    #[test]
    fn part2_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day01_test.txt")?;
        let data = parse_input(input).ok_or(anyhow!("Invalid input"))?;
        assert_eq!(count_when_passes_zero(data, 50), 6);

        Ok(())
    }

    #[test]
    fn part2() -> Result<()> {
        let input = fs::read_to_string("inputs/day01.txt")?;
        let data = parse_input(input).ok_or(anyhow!("Invalid input"))?;
        assert_eq!(count_when_passes_zero(data, 50), 6616);

        Ok(())
    }
}
