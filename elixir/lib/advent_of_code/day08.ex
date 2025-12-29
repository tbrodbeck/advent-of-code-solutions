defmodule AdventOfCode.Day08 do
  @moduledoc """
  Day 8: Playground - Connect closest junction boxes in 3D space.
  Uses libgraph for graph operations.
  """

  def parse_input(input) do
    input
    |> String.trim()
    |> String.split("\n", trim: true)
    |> Enum.map(fn line ->
      [x, y, z] = line |> String.split(",") |> Enum.map(&String.to_integer/1)
      {x, y, z}
    end)
  end

  defp distance_sq({x1, y1, z1}, {x2, y2, z2}) do
    (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) + (z1 - z2) * (z1 - z2)
  end

  defp build_sorted_edges(points) do
    n = length(points)
    indexed = points |> Enum.with_index() |> Map.new(fn {p, i} -> {i, p} end)

    for i <- 0..(n - 2)//1,
        j <- (i + 1)..(n - 1)//1 do
      {distance_sq(indexed[i], indexed[j]), i, j}
    end
    |> Enum.sort()
  end

  defp component_sizes(graph) do
    graph
    |> Graph.components()
    |> Enum.map(&length/1)
  end

  def solve_part1(input, num_connections \\ 1000) do
    points = parse_input(input)
    edges = build_sorted_edges(points)

    # Build graph with first N edges
    graph =
      edges
      |> Enum.take(num_connections)
      |> Enum.reduce(Graph.new(type: :undirected), fn {_d, i, j}, g ->
        Graph.add_edge(g, i, j)
      end)

    # Add any isolated vertices
    graph =
      Enum.reduce(0..(length(points) - 1)//1, graph, fn i, g ->
        Graph.add_vertex(g, i)
      end)

    sizes = component_sizes(graph) |> Enum.sort(:desc)
    Enum.at(sizes, 0) * Enum.at(sizes, 1) * Enum.at(sizes, 2)
  end

  def part1(input), do: solve_part1(input, 1000)

  def part2(input) do
    points = parse_input(input)
    n = length(points)
    indexed = points |> Enum.with_index() |> Map.new(fn {p, i} -> {i, p} end)
    edges = build_sorted_edges(points)

    # Start with a graph containing all vertices (isolated)
    initial_graph =
      Enum.reduce(0..(n - 1)//1, Graph.new(type: :undirected), fn i, g ->
        Graph.add_vertex(g, i)
      end)

    find_last_connection(edges, initial_graph, indexed, n)
  end

  defp find_last_connection([], _graph, _indexed, _n), do: 0

  defp find_last_connection([{_d, i, j} | rest], graph, indexed, n) do
    # Check if i and j are in different components
    in_same_component = Graph.get_shortest_path(graph, i, j) != nil

    if not in_same_component do
      graph = Graph.add_edge(graph, i, j)

      # Check if all vertices are now in one component
      if length(Graph.components(graph)) == 1 do
        {xi, _, _} = indexed[i]
        {xj, _, _} = indexed[j]
        xi * xj
      else
        find_last_connection(rest, graph, indexed, n)
      end
    else
      find_last_connection(rest, graph, indexed, n)
    end
  end
end
