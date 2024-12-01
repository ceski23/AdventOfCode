use std::collections::{BinaryHeap, HashMap};

fn parse_input(text: String) -> Option<(BinaryHeap<u32>, BinaryHeap<u32>)> {
    let mut left_heap = BinaryHeap::<u32>::new();
    let mut right_heap = BinaryHeap::<u32>::new();

    for line in text.lines() {
        let mut numbers = line.split_whitespace();

        left_heap.push(numbers.next()?.parse::<u32>().ok()?);
        right_heap.push(numbers.next()?.parse::<u32>().ok()?);
    }

    Some((left_heap, right_heap))
}

fn calc_total_distance(data: (BinaryHeap<u32>, BinaryHeap<u32>)) -> u32 {
    let (left_heap, right_heap) = data;

    left_heap
        .into_iter_sorted()
        .zip(right_heap.into_iter_sorted())
        .map(|(left, right)| left.abs_diff(right))
        .sum()
}

fn calc_similarity_score(data: (BinaryHeap<u32>, BinaryHeap<u32>)) -> u32 {
    let (left_heap, right_heap) = data;
    let mut count_map = HashMap::<&u32, u32>::new();

    for number in right_heap.iter() {
        count_map.entry(number).and_modify(|x| *x += 1).or_insert(1);
    }

    left_heap
        .iter()
        .filter_map(|number| count_map.get(number).map(|count| number * count))
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;
    use anyhow::anyhow;
    use anyhow::Result;
    use std::fs;

    #[test]
    fn part1_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day1_test.txt")?;
        let data = parse_input(input).ok_or(anyhow!("Invalid input"))?;
        assert_eq!(calc_total_distance(data), 11);

        Ok(())
    }

    #[test]
    fn part1() -> Result<()> {
        let input = fs::read_to_string("inputs/day1.txt")?;
        let data = parse_input(input).ok_or(anyhow!("Invalid input"))?;
        assert_eq!(calc_total_distance(data), 1222801);

        Ok(())
    }

    #[test]
    fn part2_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day1_test.txt")?;
        let data = parse_input(input).ok_or(anyhow!("Invalid input"))?;
        assert_eq!(calc_similarity_score(data), 31);

        Ok(())
    }

    #[test]
    fn part2() -> Result<()> {
        let input = fs::read_to_string("inputs/day1.txt")?;
        let data = parse_input(input).ok_or(anyhow!("Invalid input"))?;
        assert_eq!(calc_similarity_score(data), 22545250);

        Ok(())
    }
}
