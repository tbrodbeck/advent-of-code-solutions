defmodule AdventOfCode.Day11 do
  @moduledoc """
  Day 11: Reactor - Count paths in directed graph.

  Note: libgraph has get_paths (enumerates) but not count_paths.
  Path enumeration is O(paths), counting with memoization is O(V+E).
  """

  def parse_input(input) do
    input
    |> String.trim()
    |> String.split("\n", trim: true)
    |> Enum.reduce(%{}, fn line, graph ->
      [src, rest] = String.split(line, ":", parts: 2)
      destinations = rest |> String.trim() |> String.split(" ", trim: true)
      Map.put(graph, src, destinations)
    end)
  end

  def part1(input) do
    graph = parse_input(input)
    count_paths(graph, "you", "out", %{}) |> elem(0)
  end

  defp count_paths(_graph, node, target, memo) when node == target, do: {1, memo}

  defp count_paths(graph, node, target, memo) do
    case Map.get(memo, {node, target}) do
      nil ->
        neighbors = Map.get(graph, node, [])
        {total, memo} = Enum.reduce(neighbors, {0, memo}, fn next, {sum, m} ->
          {paths, m} = count_paths(graph, next, target, m)
          {sum + paths, m}
        end)
        {total, Map.put(memo, {node, target}, total)}
      cached ->
        {cached, memo}
    end
  end

  def part2(input) do
    graph = parse_input(input)
    memo = %{}

    {svr_dac, memo} = count_paths(graph, "svr", "dac", memo)
    {dac_fft, memo} = count_paths(graph, "dac", "fft", memo)
    {fft_out, memo} = count_paths(graph, "fft", "out", memo)

    {svr_fft, memo} = count_paths(graph, "svr", "fft", memo)
    {fft_dac, memo} = count_paths(graph, "fft", "dac", memo)
    {dac_out, _memo} = count_paths(graph, "dac", "out", memo)

    svr_dac * dac_fft * fft_out + svr_fft * fft_dac * dac_out
  end
end
