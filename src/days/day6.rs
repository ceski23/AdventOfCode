use anyhow::{anyhow, Result};
use itertools::Itertools;
use ndarray::Array2;
use std::collections::HashSet;

enum Direction {
    Up,
    Down,
    Left,
    Right,
}

fn parse_input(input: String) -> Result<Array2<String>> {
    let size = input.lines().count();
    let x = input
        .lines()
        .flat_map(|line| line.chars().map(|c| c.to_string()).collect_vec())
        .collect_vec();

    Ok(Array2::from_shape_vec((size, size), x)?)
}

fn count_visited_positions(map: Array2<String>) -> Result<usize> {
    let starting_position = map
        .iter()
        .position(|c| c == "^")
        .ok_or(anyhow!("No starting position"))?;
    let mut visited_positions = HashSet::<(isize, isize)>::new();
    let mut current_direction = Direction::Up;
    let mut current_position = (
        (starting_position / map.nrows()) as isize,
        (starting_position % map.ncols()) as isize,
    );

    loop {
        visited_positions.insert(current_position);

        let (y, x) = current_position;
        let (next_y, next_x) = match current_direction {
            Direction::Up => (y - 1, x),
            Direction::Down => (y + 1, x),
            Direction::Left => (y, x - 1),
            Direction::Right => (y, x + 1),
        };

        if next_y < 0
            || next_y >= map.nrows().try_into()?
            || next_x < 0
            || next_x >= map.ncols().try_into()?
        {
            // Guard reached the end of the map
            break;
        }

        match map[[next_y as usize, next_x as usize]].as_str() {
            "#" => match current_direction {
                Direction::Up => {
                    current_direction = Direction::Right;
                }
                Direction::Down => {
                    current_direction = Direction::Left;
                }
                Direction::Left => {
                    current_direction = Direction::Up;
                }
                Direction::Right => {
                    current_direction = Direction::Down;
                }
            },
            _ => {
                current_position = (next_y, next_x);
            }
        }
    }

    Ok(visited_positions.len())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    #[test]
    fn part1_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day6_test.txt")?;
        let map = parse_input(input)?;
        assert_eq!(count_visited_positions(map)?, 41);

        Ok(())
    }

    #[test]
    fn part1() -> Result<()> {
        let input = fs::read_to_string("inputs/day6.txt")?;
        let map = parse_input(input)?;
        assert_eq!(count_visited_positions(map)?, 4665);

        Ok(())
    }
}
