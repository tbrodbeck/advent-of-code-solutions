defmodule AdventOfCode.Day05 do
  @moduledoc """
  Day 5: Cafeteria - Check which ingredients are fresh.
  """

  def parse_input(input) do
    [ranges_part, ids_part] =
      input
      |> String.trim()
      |> String.split("\n\n", parts: 2)

    ranges =
      ranges_part
      |> String.split("\n", trim: true)
      |> Enum.map(fn line ->
        [s, e] = String.split(line, "-")
        {String.to_integer(s), String.to_integer(e)}
      end)

    ids =
      ids_part
      |> String.split("\n", trim: true)
      |> Enum.map(&String.to_integer/1)

    {ranges, ids}
  end

  def fresh?(n, ranges) do
    Enum.any?(ranges, fn {s, e} -> n >= s and n <= e end)
  end

  def part1(input) do
    {ranges, ids} = parse_input(input)
    Enum.count(ids, &fresh?(&1, ranges))
  end

  def part2(input) do
    {ranges, _ids} = parse_input(input)

    ranges
    |> Enum.sort()
    |> merge_ranges([])
    |> Enum.map(fn {s, e} -> e - s + 1 end)
    |> Enum.sum()
  end

  defp merge_ranges([], merged), do: Enum.reverse(merged)

  defp merge_ranges([{s, e} | rest], []) do
    merge_ranges(rest, [{s, e}])
  end

  defp merge_ranges([{s, e} | rest], [{ms, me} | merged]) do
    if s <= me + 1 do
      merge_ranges(rest, [{ms, max(me, e)} | merged])
    else
      merge_ranges(rest, [{s, e}, {ms, me} | merged])
    end
  end
end
