use anyhow::{anyhow, Result};
use itertools::Itertools;

type Point = (usize, usize);

fn parse_input(text: String) -> Vec<Point> {
    text.lines()
        .filter_map(|line| {
            let (x, y) = line.split_once(",")?;
            Some((x.parse::<usize>().ok()?, y.parse::<usize>().ok()?))
        })
        .collect_vec()
}

fn calc_area((x1, y1): &Point, (x2, y2): &Point) -> u64 {
    let height = y1.max(y2) - y1.min(y2) + 1;
    let width = x1.max(x2) - x1.min(x2) + 1;

    (width * height).try_into().unwrap()
}

fn find_largest_rectangle(text: String) -> Result<u64> {
    let points = parse_input(text);
    let areas = points.iter().combinations_with_replacement(2).map(|pair| {
        let (point_a, point_b) = pair.iter().next_tuple().unwrap();

        calc_area(point_a, point_b)
    });

    areas.max().ok_or(anyhow!("Couldn't find maximum"))
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    #[test]
    fn part1_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day09_test.txt")?;
        assert_eq!(find_largest_rectangle(input)?, 50);

        Ok(())
    }

    #[test]
    fn part1() -> Result<()> {
        let input = fs::read_to_string("inputs/day09.txt")?;
        assert_eq!(find_largest_rectangle(input)?, 4769758290);

        Ok(())
    }
}
