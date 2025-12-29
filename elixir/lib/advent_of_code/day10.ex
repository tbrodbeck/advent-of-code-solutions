defmodule AdventOfCode.Day10 do
  @moduledoc """
  Day 10: Diagram Solver - BFS state exploration and linear constraint minimization.
  """

  def parse_input(input) do
    input
    |> String.trim()
    |> String.split("\n", trim: true)
    |> Enum.map(&parse_line/1)
  end

  defp parse_line(line) do
    parts = String.split(line, " ")

    diagram_str = parts |> hd() |> String.trim_leading("[") |> String.trim_trailing("]")
    diagram =
      diagram_str
      |> String.graphemes()
      |> Enum.with_index()
      |> Enum.filter(fn {ch, _} -> ch == "#" end)
      |> Enum.map(fn {_, idx} -> idx end)
      |> MapSet.new()

    {schematics_strs, [joltage_str]} = Enum.split(tl(parts), -1)

    schematics =
      schematics_strs
      |> Enum.map(fn s ->
        s
        |> String.trim_leading("(")
        |> String.trim_trailing(")")
        |> String.split(",")
        |> Enum.map(&String.to_integer/1)
      end)
      |> Enum.sort_by(&length/1)

    joltage =
      joltage_str
      |> String.trim_leading("{")
      |> String.trim_trailing("}")
      |> String.split(",")
      |> Enum.map(&String.to_integer/1)

    {diagram, schematics, joltage}
  end

  def part1(input) do
    parsed = parse_input(input)
    Enum.sum(for {diagram, schematics, _joltage} <- parsed, do: solve_diagram(diagram, schematics))
  end

  defp solve_diagram(diagram, schematics) do
    solve_bfs([{diagram, 0}], schematics, MapSet.new([diagram]))
  end

  defp solve_bfs([], _schematics, _seen), do: :infinity

  defp solve_bfs([{diagram, level} | rest], schematics, seen) do
    if MapSet.size(diagram) == 0 do
      level
    else
      {new_states, seen} =
        Enum.reduce(schematics, {[], seen}, fn schematic, {states, seen} ->
          new_diagram = apply_schematic(diagram, schematic)
          if MapSet.member?(seen, new_diagram) do
            {states, seen}
          else
            {[{new_diagram, level + 1} | states], MapSet.put(seen, new_diagram)}
          end
        end)
      solve_bfs(rest ++ Enum.reverse(new_states), schematics, seen)
    end
  end

  defp apply_schematic(diagram, schematic) do
    Enum.reduce(schematic, diagram, fn action, d ->
      if MapSet.member?(d, action), do: MapSet.delete(d, action), else: MapSet.put(d, action)
    end)
  end

  def part2(input) do
    parsed = parse_input(input)
    Enum.sum(for {_diagram, schematics, joltages} <- parsed, do: solve_min_sum(schematics, joltages))
  end

  defp solve_min_sum(schematics, joltages) do
    n = length(schematics)

    # Build constraint matrix: A[j][i] = 1 if joltage index j is in schematic i
    matrix = joltages
      |> Enum.with_index()
      |> Enum.map(fn {target, jolt_idx} ->
        coeffs = for i <- 0..(n-1), do: (if jolt_idx in Enum.at(schematics, i), do: 1, else: 0)
        coeffs ++ [target]
      end)

    # Compute RREF
    {rref, pivot_cols} = compute_rref(matrix, n)
    free_cols = Enum.to_list(0..(n-1)) -- pivot_cols

    if free_cols == [] do
      # Determined system - direct solution
      case extract_solution(rref, pivot_cols, n, List.duplicate(0, n)) do
        {:ok, sol} -> Enum.sum(sol)
        :invalid -> 0
      end
    else
      # Underdetermined - search free variables
      max_val = Enum.max(joltages)
      find_min_solution(rref, pivot_cols, free_cols, n, max_val)
    end
  end

  defp compute_rref(matrix, n) do
    m = length(matrix)
    do_rref(matrix, n, m, 0, 0, [])
  end

  defp do_rref(matrix, n, m, row, col, pivots) when row >= m or col >= n do
    {matrix, Enum.reverse(pivots)}
  end

  defp do_rref(matrix, n, m, row, col, pivots) do
    # Find pivot in column
    pivot_row = Enum.find(row..(m-1), fn r -> Enum.at(Enum.at(matrix, r), col) != 0 end)

    if pivot_row == nil do
      do_rref(matrix, n, m, row, col + 1, pivots)
    else
      # Swap rows
      matrix = if pivot_row != row do
        r1 = Enum.at(matrix, row)
        r2 = Enum.at(matrix, pivot_row)
        matrix |> List.replace_at(row, r2) |> List.replace_at(pivot_row, r1)
      else
        matrix
      end

      pivot_val = Enum.at(Enum.at(matrix, row), col)
      pivot_row_data = Enum.at(matrix, row)

      # Eliminate all other rows
      matrix = Enum.with_index(matrix) |> Enum.map(fn {r, i} ->
        if i == row do
          r
        else
          factor = Enum.at(r, col)
          if factor == 0 do
            r
          else
            Enum.zip(r, pivot_row_data) |> Enum.map(fn {a, b} ->
              a * pivot_val - b * factor
            end)
          end
        end
      end)

      do_rref(matrix, n, m, row + 1, col + 1, [col | pivots])
    end
  end

  defp extract_solution(rref, pivot_cols, n, free_vals) do
    solution = free_vals

    Enum.reduce_while(Enum.with_index(pivot_cols), {:ok, solution}, fn {pcol, ridx}, {:ok, sol} ->
      row = Enum.at(rref, ridx)
      pivot = Enum.at(row, pcol)
      rhs = List.last(row)

      # Sum contributions from free variables
      free_sum = Enum.reduce(0..(n-1), 0, fn c, acc ->
        if c != pcol and c not in pivot_cols do
          acc + Enum.at(row, c) * Enum.at(sol, c)
        else
          acc
        end
      end)

      remainder = rhs - free_sum

      if rem(remainder, pivot) != 0 do
        {:halt, :invalid}
      else
        val = div(remainder, pivot)
        if val < 0 do
          {:halt, :invalid}
        else
          {:cont, {:ok, List.replace_at(sol, pcol, val)}}
        end
      end
    end)
  end

  defp find_min_solution(rref, pivot_cols, free_cols, n, max_val) do
    # Generate all combinations of free variable values and find minimum valid solution
    ranges = Enum.map(free_cols, fn _ -> 0..max_val end)

    combinations(ranges)
    |> Stream.map(fn free_vals_list ->
      # Build full solution vector with free values set
      base = List.duplicate(0, n)
      base = Enum.zip(free_cols, free_vals_list) |> Enum.reduce(base, fn {col, val}, acc ->
        List.replace_at(acc, col, val)
      end)

      case extract_solution(rref, pivot_cols, n, base) do
        {:ok, sol} -> Enum.sum(sol)
        :invalid -> nil
      end
    end)
    |> Stream.filter(&(&1 != nil))
    |> Enum.min(fn -> 0 end)
  end

  defp combinations([]), do: [[]]
  defp combinations([range | rest]) do
    for val <- range, tail <- combinations(rest), do: [val | tail]
  end
end
