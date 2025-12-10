use anyhow::Result;
use itertools::Itertools;
use pathfinding::prelude::bfs;
use regress::Regex;
use std::{collections::HashMap, iter::repeat_n};

fn toggle_lights(lights: String, button: Vec<usize>) -> String {
    lights
        .chars()
        .enumerate()
        .map(|(index, light)| match (button.contains(&index), light) {
            (true, '.') => '#',
            (true, '#') => '.',
            _ => light,
        })
        .collect()
}

fn find_least_button_presses(text: String) -> Result<usize> {
    let lights_pattern = Regex::new(r"\[([\.#]+)\]")?;
    let button_pattern = Regex::new(r"\((\d[\d(?:\d,)]*)\) ")?;
    let result = text
        .lines()
        .map(|line| {
            let target_light = &line[lights_pattern.find(line).unwrap().group(1).unwrap()];
            let buttons = button_pattern
                .find_iter(line)
                .map(|button_match| {
                    let text = &line[button_match.group(1).unwrap()];
                    text.split(',')
                        .map(|number| number.parse::<usize>().unwrap())
                        .collect_vec()
                })
                .collect_vec();

            let possible_nodes: Vec<String> = repeat_n(['.', '#'], target_light.len())
                .multi_cartesian_product()
                .map(|chars| chars.iter().collect())
                .collect();

            let mut adjacency_list: HashMap<String, Vec<String>> = possible_nodes
                .iter()
                .map(|node| (node.clone(), Vec::new()))
                .collect();

            for node in &possible_nodes {
                for button in &buttons {
                    let target = toggle_lights(node.clone(), button.clone());

                    if let Some(neighbors) = adjacency_list.get_mut(&target) {
                        neighbors.push(node.clone());
                    }
                    if let Some(neighbors) = adjacency_list.get_mut(node) {
                        neighbors.push(target);
                    }
                }
            }

            let start: String = repeat_n('.', target_light.len()).collect();

            let shortest_path = bfs(
                &start,
                |current_node| adjacency_list.get(current_node).unwrap().iter().cloned(),
                |current_node| current_node == target_light,
            )
            .unwrap();

            shortest_path.len() - 1
        })
        .sum();

    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    #[test]
    fn part1_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day10_test.txt")?;
        assert_eq!(find_least_button_presses(input)?, 7);

        Ok(())
    }

    #[test]
    fn part1() -> Result<()> {
        let input = fs::read_to_string("inputs/day10.txt")?;
        assert_eq!(find_least_button_presses(input)?, 558);

        Ok(())
    }
}
