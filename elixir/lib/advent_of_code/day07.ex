defmodule AdventOfCode.Day07 do
  @moduledoc """
  Day 7: Laboratories - Traverse tachyon manifold grid.
  """

  def parse_input(input) do
    grid =
      input
      |> String.trim()
      |> String.split("\n", trim: true)
      |> Enum.map(&String.graphemes/1)

    rows = length(grid)
    cols = length(Enum.at(grid, 0))
    start_col = grid |> Enum.at(0) |> Enum.find_index(&(&1 == "S"))

    {grid, start_col, rows, cols}
  end

  defp at(grid, row, col) do
    grid |> Enum.at(row) |> Enum.at(col)
  end

  def part1(input) do
    {grid, start_col, rows, cols} = parse_input(input)
    visited = traverse(grid, rows, cols, 1, start_col, MapSet.new())
    MapSet.size(visited)
  end

  defp traverse(_grid, rows, _cols, row, _col, visited) when row < 0 or row >= rows, do: visited
  defp traverse(_grid, _rows, cols, _row, col, visited) when col < 0 or col >= cols, do: visited

  defp traverse(grid, rows, cols, row, col, visited) do
    if MapSet.member?(visited, {row, col}) do
      visited
    else
      char = at(grid, row, col)

      case char do
        "^" ->
          visited = MapSet.put(visited, {row, col})
          visited = traverse(grid, rows, cols, row + 1, col - 1, visited)
          traverse(grid, rows, cols, row + 1, col + 1, visited)

        c when c in [".", "S"] ->
          traverse(grid, rows, cols, row + 1, col, visited)

        _ ->
          visited
      end
    end
  end

  def part2(input) do
    {grid, start_col, rows, cols} = parse_input(input)
    {count, _memo} = count_paths(grid, rows, cols, 0, start_col, %{})
    count
  end

  defp count_paths(_grid, rows, _cols, row, _col, memo) when row >= rows, do: {0, memo}
  defp count_paths(_grid, _rows, cols, _row, col, memo) when col < 0 or col >= cols, do: {0, memo}

  defp count_paths(grid, rows, cols, row, col, memo) do
    if row == rows - 1 do
      {1, memo}
    else
      case Map.get(memo, {row, col}) do
        nil ->
          char = at(grid, row, col)

          {result, memo} =
            case char do
              "^" ->
                {left, memo} = count_paths(grid, rows, cols, row + 1, col - 1, memo)
                {right, memo} = count_paths(grid, rows, cols, row + 1, col + 1, memo)
                {left + right, memo}

              c when c in [".", "S"] ->
                count_paths(grid, rows, cols, row + 1, col, memo)

              _ ->
                {0, memo}
            end

          {result, Map.put(memo, {row, col}, result)}

        cached ->
          {cached, memo}
      end
    end
  end
end
