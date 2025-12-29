defmodule AdventOfCode.Day02Test do
  use ExUnit.Case

  alias AdventOfCode.Day02

  @example_input "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

  describe "part1/1" do
    test "solves example input" do
      assert Day02.part1(@example_input) == 1_227_775_554
    end

    test "is_invalid detects repeated twice" do
      assert Day02.invalid?(55)
      assert Day02.invalid?(6464)
      assert Day02.invalid?(123123)
      assert Day02.invalid?(99)
      refute Day02.invalid?(101)
    end
  end

  describe "part2/1" do
    test "solves example input" do
      assert Day02.part2(@example_input) == 4_174_379_265
    end

    test "is_invalid_v2 detects repeated at least twice" do
      assert Day02.invalid_v2?(111)
      assert Day02.invalid_v2?(1212121212)
      assert Day02.invalid_v2?(565656)
      assert Day02.invalid_v2?(824824824)
      refute Day02.invalid_v2?(101)
    end
  end
end
