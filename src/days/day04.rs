use anyhow::Result;
use itertools::Itertools;

fn parse_input(text: String) -> Result<Vec<Vec<bool>>> {
    let diagram = text
        .lines()
        .map(|line| line.chars().map(|char| char == '@').collect_vec())
        .collect_vec();

    Ok(diagram)
}

fn is_roll_accessible(diagram: &[Vec<bool>], x: usize, y: usize) -> bool {
    let neighbor_count = (-1..=1)
        .cartesian_product(-1..=1)
        .filter(|&(dy, dx)| dy != 0 || dx != 0)
        .filter_map(|(dy, dx)| {
            let ny = y.checked_add_signed(dy)?;
            let nx = x.checked_add_signed(dx)?;
            diagram.get(ny)?.get(nx)
        })
        .filter(|&&is_roll| is_roll)
        .count();

    neighbor_count < 4
}

fn find_accessible_rolls(diagram: &[Vec<bool>]) -> Option<Vec<(usize, usize)>> {
    let rolls = (0..diagram.len())
        .cartesian_product(0..diagram[0].len())
        .filter(|(y, x)| diagram[*y][*x] && is_roll_accessible(diagram, *x, *y))
        .collect_vec();

    (!rolls.is_empty()).then_some(rolls)
}

fn count_all_possible_accessible_rolls(mut diagram: Vec<Vec<bool>>) -> usize {
    let mut count = 0;

    while let Some(accessible_rolls_indicies) = find_accessible_rolls(&diagram) {
        count += accessible_rolls_indicies.len();

        for (y, x) in accessible_rolls_indicies {
            diagram[y][x] = false
        }
    }

    count
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    #[test]
    fn part1_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day04_test.txt")?;
        let data = parse_input(input)?;
        assert_eq!(find_accessible_rolls(&data).unwrap_or_default().len(), 13);

        Ok(())
    }

    #[test]
    fn part1() -> Result<()> {
        let input = fs::read_to_string("inputs/day04.txt")?;
        let data = parse_input(input)?;
        assert_eq!(find_accessible_rolls(&data).unwrap_or_default().len(), 1474);

        Ok(())
    }

    #[test]
    fn part2_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day04_test.txt")?;
        let data = parse_input(input)?;
        assert_eq!(count_all_possible_accessible_rolls(data), 43);

        Ok(())
    }

    #[test]
    fn part2() -> Result<()> {
        let input = fs::read_to_string("inputs/day04.txt")?;
        let data = parse_input(input)?;
        assert_eq!(count_all_possible_accessible_rolls(data), 8910);

        Ok(())
    }
}
