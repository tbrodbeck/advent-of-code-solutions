defmodule AdventOfCode.Day04 do
  @moduledoc """
  Day 4: Printing Department - Count accessible paper rolls.
  """

  @directions [{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}]

  def parse_input(input) do
    input
    |> String.trim()
    |> String.split("\n", trim: true)
    |> Enum.map(&String.graphemes/1)
  end

  def count_neighbors(grid, r, c) do
    rows = length(grid)
    cols = length(Enum.at(grid, 0))

    Enum.count(@directions, fn {dr, dc} ->
      nr = r + dr
      nc = c + dc

      nr >= 0 and nr < rows and nc >= 0 and nc < cols and
        Enum.at(Enum.at(grid, nr), nc) == "@"
    end)
  end

  defp accessible?(grid, r, c) do
    Enum.at(Enum.at(grid, r), c) == "@" and count_neighbors(grid, r, c) < 4
  end

  def part1(input) do
    grid = parse_input(input)
    rows = length(grid)
    cols = length(Enum.at(grid, 0))

    for r <- 0..(rows - 1)//1, c <- 0..(cols - 1)//1, accessible?(grid, r, c), reduce: 0 do
      acc -> acc + 1
    end
  end

  def part2(input) do
    grid = parse_input(input)
    remove_loop(grid, 0)
  end

  defp remove_loop(grid, total) do
    rows = length(grid)
    cols = length(Enum.at(grid, 0))

    to_remove =
      for r <- 0..(rows - 1)//1,
          c <- 0..(cols - 1)//1,
          accessible?(grid, r, c),
          do: {r, c}

    case to_remove do
      [] ->
        total

      positions ->
        new_grid =
          Enum.reduce(positions, grid, fn {r, c}, g ->
            List.update_at(g, r, fn row -> List.replace_at(row, c, ".") end)
          end)

        remove_loop(new_grid, total + length(positions))
    end
  end
end
