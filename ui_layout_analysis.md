# UI Layout Analysis for Elias Game

## Window Dimensions
- Width: 800px
- Height: 600px

## Difficulty Selection Screen Layout

### Vertical Positioning:
1. Title: y = WINDOW_HEIGHT//4 - 40 = 600//4 - 40 = 150 - 40 = 110px
2. Difficulty label: y = WINDOW_HEIGHT//2 - 80 = 600//2 - 80 = 300 - 80 = 220px
3. Difficulty buttons (y = WINDOW_HEIGHT//2 - 40 = 300 - 40 = 260px)
   - Height: 50px
   - Bottom: 260 + 50 = 310px
4. Difficulty description: y = WINDOW_HEIGHT//2 - 10 = 300 - 10 = 290px
5. Time label: y = WINDOW_HEIGHT//2 + 5 = 300 + 5 = 305px
6. Time dropdown: 
   - y = WINDOW_HEIGHT//2 + 30 = 300 + 30 = 330px
   - Height: 40px
   - Bottom: 330 + 40 = 370px
7. Confirm button: 
   - y = WINDOW_HEIGHT//2 + 100 = 300 + 100 = 400px
   - Height: 50px
   - Bottom: 400 + 50 = 450px
8. Back button: 
   - y = 20px
   - Height: 40px
   - Bottom: 20 + 40 = 60px

### Overlap Analysis for Difficulty Screen:
- Title (110px) does not overlap with difficulty label (220px) - OK
- Difficulty label (220px) does not overlap with difficulty buttons (260px) - OK
- Difficulty buttons (260-310px) overlap with difficulty description (290px) - OVERLAP!
- Difficulty description (290px) overlaps with time label (305px) - OVERLAP!
- Time label (305px) overlaps with time dropdown (330-370px) - OK (some spacing)
- Time dropdown (330-370px) does not overlap with confirm button (400-450px) - OK

## Word Management Screen Layout

### Vertical Positioning:
1. Title: y = 40px
   - Large font (~48px) - Bottom: ~88px
2. Word count: y = 70px
3. Difficulty counts: y = 90px
4. Input field: 
   - y = 100px
   - Height: 40px
   - Bottom: 140px
5. Difficulty label: y = 130px
6. Difficulty dropdown: 
   - y = 150px
   - Height: 40px
   - Bottom: 190px
7. Word list: 
   - y = 200px
   - Height: WINDOW_HEIGHT - 270 = 600 - 270 = 330px
   - Bottom: 200 + 330 = 530px
8. Buttons (right side):
   - Back button: y = 20px, height = 40px, bottom = 60px
   - Add word: y = 100px, height = 40px, bottom = 140px
   - Edit word: y = 150px, height = 40px, bottom = 190px
   - Delete word: y = 200px, height = 40px, bottom = 240px
   - Save word: y = 250px, height = 40px, bottom = 290px
   - Cancel edit: y = 300px, height = 40px, bottom = 340px

### Overlap Analysis for Management Screen:
- Title (40-88px) overlaps with word count (70px) and difficulty counts (90px) - OVERLAP!
- Input field (100-140px) overlaps with difficulty label (130px) - OVERLAP!
- Difficulty label (130px) overlaps with difficulty dropdown (150-190px) - OVERLAP!
- Difficulty dropdown (150-190px) overlaps with word list (200-530px) - OK (small overlap)
- Right-side buttons have proper spacing - OK

## Dropdown Overlay Analysis:
The dropdown implementation draws options in a separate area below the dropdown box, 
which should properly overlay other elements since it's drawn last in the draw order.

However, there's an issue with the word list scrollbar potentially overlapping with 
the right-side buttons in the management screen.

## Recommendations:
1. Adjust difficulty screen vertical spacing to eliminate overlaps
2. Adjust management screen vertical spacing to eliminate overlaps
3. Ensure dropdown menus properly overlay other elements (current implementation looks OK)