defmodule AdventOfCode.Day09 do
  @moduledoc """
  Day 9: Polygon Rectangles - Find largest rectangles in/from polygon vertices.
  """

  def parse_input(input) do
    input
    |> String.trim()
    |> String.split("\n", trim: true)
    |> Enum.map(fn line ->
      [x, y] = line |> String.split(",") |> Enum.map(&String.to_integer/1)
      {x, y}
    end)
  end

  def part1(input) do
    vertices = parse_input(input)
    n = length(vertices)

    for i <- 0..(n - 2)//1,
        j <- (i + 1)..(n - 1)//1 do
      {x1, y1} = Enum.at(vertices, i)
      {x2, y2} = Enum.at(vertices, j)
      (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
    end
    |> Enum.max()
  end

  def part2(input) do
    vertices = parse_input(input)
    n = length(vertices)

    # Create closed ring for Geo.Polygon (first point repeated at end)
    ring = vertices ++ [hd(vertices)]
    polygon = %Geo.Polygon{coordinates: [ring]}

    # Check all pairs of vertices as potential rectangle corners
    pairs = for i <- 0..(n - 1)//1, j <- 0..(n - 1)//1, i != j, do: {i, j}

    pairs
    |> Task.async_stream(
      fn {i, j} ->
        {x1, y1} = Enum.at(vertices, i)
        {x2, y2} = Enum.at(vertices, j)

        # Create rectangle as closed polygon
        rect_ring = [{x1, y1}, {x1, y2}, {x2, y2}, {x2, y1}, {x1, y1}]
        rect = %Geo.Polygon{coordinates: [rect_ring]}

        if Topo.contains?(polygon, rect) do
          (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        else
          0
        end
      end,
      max_concurrency: System.schedulers_online() * 2,
      timeout: :infinity
    )
    |> Enum.map(fn {:ok, v} -> v end)
    |> Enum.max()
  end
end