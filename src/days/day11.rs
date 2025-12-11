use pathfinding::prelude::count_paths;
use std::collections::HashMap;

fn count_signal_paths(text: String) -> usize {
    let devices: HashMap<&str, Vec<String>> = text
        .lines()
        .map(|line| {
            let (device_name, outputs_string) = line.split_once(": ").unwrap();
            let outputs = outputs_string
                .split_whitespace()
                .map(|s| s.to_owned())
                .collect();

            (device_name, outputs)
        })
        .collect();

    count_paths(
        "you".to_string(),
        |current_node| devices.get(current_node.as_str()).unwrap().iter().cloned(),
        |current_node| current_node == "out",
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use anyhow::Result;
    use std::fs;

    #[test]
    fn part1_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day11_test.txt")?;
        assert_eq!(count_signal_paths(input), 5);

        Ok(())
    }

    #[test]
    fn part1() -> Result<()> {
        let input = fs::read_to_string("inputs/day11.txt")?;
        assert_eq!(count_signal_paths(input), 690);

        Ok(())
    }
}
