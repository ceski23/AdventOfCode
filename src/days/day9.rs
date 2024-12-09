use anyhow::Result;
use itertools::Itertools;

fn calculate_filesystem_checksum(memory: String) -> Result<usize> {
    let disk_map = memory.chars().filter_map(|c| c.to_digit(10));
    let files = disk_map.clone().step_by(2).collect_vec();
    let mut file_blocks = files
        .iter()
        .enumerate()
        .flat_map(|(index, &file_id)| std::iter::repeat_n(index, file_id.try_into().unwrap()));
    let checksum = disk_map
        .enumerate()
        .flat_map(|(index, count)| {
            (0..count)
                .filter_map(|_| {
                    if index % 2 == 0 {
                        file_blocks.next()
                    } else {
                        file_blocks.next_back()
                    }
                })
                .collect_vec()
        })
        .enumerate()
        .fold(0, |sum, (index, file_id)| sum + (index * file_id));

    Ok(checksum)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    #[test]
    fn part1_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day9_test.txt")?;
        assert_eq!(calculate_filesystem_checksum(input)?, 1928);

        Ok(())
    }

    #[test]
    fn part1() -> Result<()> {
        let input = fs::read_to_string("inputs/day9.txt")?;
        assert_eq!(calculate_filesystem_checksum(input)?, 6430446922192);

        Ok(())
    }
}
