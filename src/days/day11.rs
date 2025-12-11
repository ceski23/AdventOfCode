use std::collections::HashMap;

fn parse_input(text: &str) -> HashMap<&str, Vec<String>> {
    text.lines()
        .map(|line| {
            let (device_name, outputs_string) = line.split_once(": ").unwrap();
            let outputs = outputs_string
                .split_whitespace()
                .map(|s| s.to_owned())
                .collect();

            (device_name, outputs)
        })
        .collect()
}

fn dfs_memo(
    src: &str,
    dst: &str,
    graph: &HashMap<&str, Vec<String>>,
    memo: &mut HashMap<(String, String), usize>,
) -> usize {
    if src == dst {
        return 1;
    }

    let key = (src.to_string(), dst.to_string());

    if let Some(&count) = memo.get(&key) {
        return count;
    }

    let mut result = 0;

    if let Some(neighbours) = graph.get(src) {
        for neighbour in neighbours {
            result += dfs_memo(neighbour.as_str(), dst, graph, memo);
        }
    }

    memo.insert(key, result);
    result
}

fn count_signal_paths(text: String) -> usize {
    let graph = parse_input(&text);
    let mut memo = HashMap::new();

    dfs_memo("you", "out", &graph, &mut memo)
}

fn find_signal_paths(text: String) -> usize {
    let graph = parse_input(&text);
    let mut memo = HashMap::new();

    let svr_dac_fft_out = dfs_memo("svr", "dac", &graph, &mut memo)
        * dfs_memo("dac", "fft", &graph, &mut memo)
        * dfs_memo("fft", "out", &graph, &mut memo);

    let svr_fft_dac_out = dfs_memo("svr", "fft", &graph, &mut memo)
        * dfs_memo("fft", "dac", &graph, &mut memo)
        * dfs_memo("dac", "out", &graph, &mut memo);

    svr_dac_fft_out + svr_fft_dac_out
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

    #[test]
    fn part2_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day11_test2.txt")?;
        assert_eq!(find_signal_paths(input), 2);

        Ok(())
    }

    #[test]
    fn part2() -> Result<()> {
        let input = fs::read_to_string("inputs/day11.txt")?;
        assert_eq!(find_signal_paths(input), 557332758684000);

        Ok(())
    }
}
