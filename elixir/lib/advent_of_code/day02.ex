defmodule AdventOfCode.Day02 do
  @moduledoc """
  Day 2: Gift Shop - Find invalid IDs (digits repeated).
  """

  def parse_input(input) do
    input
    |> String.trim()
    |> String.split(",")
    |> Enum.map(&parse_range/1)
  end

  defp parse_range(range_str) do
    [start, finish] = range_str |> String.trim() |> String.split("-")
    {String.to_integer(start), String.to_integer(finish)}
  end

  @doc "Check if ID is same sequence repeated exactly twice."
  def invalid?(n) do
    s = Integer.to_string(n)
    len = String.length(s)

    rem(len, 2) == 0 and
      String.slice(s, 0, div(len, 2)) == String.slice(s, div(len, 2), len)
  end

  @doc "Check if ID is same sequence repeated at least twice."
  def invalid_v2?(n) do
    s = Integer.to_string(n)
    len = String.length(s)
    half = div(len, 2)

    half >= 1 and Enum.any?(1..half//1, fn rep_len ->
      rem(len, rep_len) == 0 and
        String.duplicate(String.slice(s, 0, rep_len), div(len, rep_len)) == s
    end)
  end

  defp sum_invalid_ids(input, invalid_fn) do
    input
    |> parse_input()
    |> Enum.flat_map(fn {start, finish} -> start..finish end)
    |> Enum.filter(invalid_fn)
    |> Enum.sum()
  end

  def part1(input), do: sum_invalid_ids(input, &invalid?/1)
  def part2(input), do: sum_invalid_ids(input, &invalid_v2?/1)
end
