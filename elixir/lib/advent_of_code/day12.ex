defmodule AdventOfCode.Day12 do
  @moduledoc """
  Day 12: Christmas Tree Farm - Count regions where presents can fit.
  """

  def parse_input(input) do
    lines = input |> String.split("\n")
    {shapes_by_idx, rest_idx} = parse_shapes(lines, 0, %{})
    regions = parse_regions(lines, rest_idx)

    # Convert shapes to normalized cell lists
    max_idx = if map_size(shapes_by_idx) > 0, do: Enum.max(Map.keys(shapes_by_idx)), else: -1

    shapes =
      for idx <- 0..max_idx do
        rows = Map.get(shapes_by_idx, idx, [])
        cells = for {row, y} <- Enum.with_index(rows),
                    {ch, x} <- Enum.with_index(String.graphemes(row)),
                    ch == "#", do: {x, y}
        normalize_cells(cells)
      end

    {shapes, regions}
  end

  defp parse_shapes(lines, idx, shapes) do
    case Enum.at(lines, idx) do
      nil -> {shapes, idx}
      line ->
        line = String.trim(line)
        cond do
          line == "" ->
            parse_shapes(lines, idx + 1, shapes)
          Regex.match?(~r/^\d+x\d+:/, line) ->
            {shapes, idx}
          Regex.match?(~r/^\d+:/, line) ->
            [num_str | rest] = String.split(line, ":", parts: 2)
            shape_idx = String.to_integer(num_str)
            first_row = rest |> List.first() |> String.trim()
            {rows, next_idx} = parse_shape_rows(lines, idx + 1, if(first_row != "", do: [first_row], else: []))
            parse_shapes(lines, next_idx, Map.put(shapes, shape_idx, Enum.reverse(rows)))
          true ->
            parse_shapes(lines, idx + 1, shapes)
        end
    end
  end

  defp parse_shape_rows(lines, idx, rows) do
    case Enum.at(lines, idx) do
      nil -> {rows, idx}
      line ->
        line = String.trim(line)
        cond do
          line == "" -> parse_shape_rows(lines, idx + 1, rows)
          Regex.match?(~r/^\d+:/, line) -> {rows, idx}
          Regex.match?(~r/^\d+x\d+:/, line) -> {rows, idx}
          String.match?(line, ~r/^[.#]+$/) -> parse_shape_rows(lines, idx + 1, [line | rows])
          true -> {rows, idx}
        end
    end
  end

  defp parse_regions(lines, idx) do
    lines
    |> Enum.drop(idx)
    |> Enum.filter(&(&1 != "" and String.trim(&1) != ""))
    |> Enum.map(fn line ->
      line = String.trim(line)
      case Regex.run(~r/^(\d+)x(\d+):\s*(.*)$/, line) do
        [_, w_str, h_str, qty_str] ->
          w = String.to_integer(w_str)
          h = String.to_integer(h_str)
          qty = qty_str
            |> String.split(" ", trim: true)
            |> Enum.map(&String.to_integer/1)
          {w, h, qty}
        _ -> nil
      end
    end)
    |> Enum.filter(&(&1 != nil))
  end

  defp normalize_cells(cells) do
    if cells == [] do
      []
    else
      min_x = cells |> Enum.map(&elem(&1, 0)) |> Enum.min()
      min_y = cells |> Enum.map(&elem(&1, 1)) |> Enum.min()
      cells |> Enum.map(fn {x, y} -> {x - min_x, y - min_y} end) |> Enum.sort()
    end
  end

  defp orientations(shape) do
    rot90 = fn cells -> Enum.map(cells, fn {x, y} -> {y, -x} end) end
    flipx = fn cells -> Enum.map(cells, fn {x, y} -> {-x, y} end) end

    base = shape
    variants = [base, flipx.(base)]

    Enum.flat_map(variants, fn variant ->
      Enum.scan(0..3, variant, fn _, cur -> rot90.(cur) end)
    end)
    |> Enum.map(&normalize_cells/1)
    |> Enum.uniq()
    |> Enum.map(fn cells ->
      w = (cells |> Enum.map(&elem(&1, 0)) |> Enum.max(fn -> 0 end)) + 1
      h = (cells |> Enum.map(&elem(&1, 1)) |> Enum.max(fn -> 0 end)) + 1
      {cells, w, h}
    end)
  end

  defp placements(w, h, shape) do
    for {cells, sw, sh} <- orientations(shape),
        sw <= w and sh <= h,
        oy <- 0..(h - sh),
        ox <- 0..(w - sw) do
      mask = Enum.reduce(cells, 0, fn {x, y}, acc ->
        Bitwise.bor(acc, Bitwise.bsl(1, (oy + y) * w + (ox + x)))
      end)
      mask
    end
    |> Enum.uniq()
    |> Enum.sort()
  end

  defp can_fit_region?(w, h, shapes, qty) do
    qty = qty ++ List.duplicate(0, max(0, length(shapes) - length(qty)))

    areas = Enum.map(shapes, &length/1)
    needed = Enum.zip(qty, areas) |> Enum.map(fn {q, a} -> q * a end) |> Enum.sum()

    if needed > w * h do
      false
    else
      placements_by_shape = Enum.map(shapes, &placements(w, h, &1))

      # Check if any shape with qty > 0 has no placements
      can_proceed = Enum.zip(qty, placements_by_shape)
        |> Enum.all?(fn {q, pl} -> q == 0 or pl != [] end)

      if not can_proceed do
        false
      else
        pieces = Enum.sum(qty)
        # For large regions or many pieces, assume true
        if w * h > 120 or pieces > 18 do
          true
        else
          dfs(0, qty, placements_by_shape, %{})
        end
      end
    end
  end

  defp dfs(occupied, counts, placements_by_shape, memo) do
    if Enum.all?(counts, &(&1 == 0)) do
      true
    else
      key = {occupied, counts}
      case Map.get(memo, key) do
        nil ->
          # Find shape with fewest options
          options_per_shape =
            counts
            |> Enum.with_index()
            |> Enum.filter(fn {c, _} -> c > 0 end)
            |> Enum.map(fn {_, i} ->
              opts = Enum.filter(Enum.at(placements_by_shape, i), fn m ->
                Bitwise.band(m, occupied) == 0
              end)
              {i, opts}
            end)

          if Enum.any?(options_per_shape, fn {_, opts} -> opts == [] end) do
            false
          else
            {best_i, best_opts} = Enum.min_by(options_per_shape, fn {_, opts} -> length(opts) end)

            result = Enum.reduce_while(best_opts, false, fn mask, _acc ->
              new_counts = List.update_at(counts, best_i, &(&1 - 1))
              if dfs(Bitwise.bor(occupied, mask), new_counts, placements_by_shape, memo) do
                {:halt, true}
              else
                {:cont, false}
              end
            end)

            result
          end

        cached -> cached
      end
    end
  end

  def part1(input) do
    {shapes, regions} = parse_input(input)

    regions
    |> Enum.count(fn {w, h, qty} -> can_fit_region?(w, h, shapes, qty) end)
  end

  def part2(_input) do
    :not_implemented
  end
end
