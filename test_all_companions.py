import sys
import tkinter as tk

def test_character_initialization():
    import desktop_companion as dc
    
    characters = ["Beru", "Igris", "Cat", "Spiderman", "Puppy"]
    print("Testing character initialization for:", characters)
    
    # We create a hidden root to satisfy PhotoImage
    root = tk.Tk()
    root.withdraw()
    
    for char in characters:
        renderer = dc.UniversalCompanionRenderer(char)
        print(f"[{char}] Renderer initialized successfully: name={renderer.char_name}")
        
        # Test drawing idle pose
        img = renderer.render(frame=0, emotion="idle")
        assert img is not None, f"Failed to get IDLE image for {char}"
        print(f"[{char}] IDLE frame generated: {img.width()}x{img.height()}")
        
        # Test specific poses
        if char == "Spiderman":
            swing_img = renderer.spidey_renderer.draw_web_swing(1)
            assert swing_img is not None
            crawl_img = renderer.spidey_renderer.draw_wall_crawl(1)
            assert crawl_img is not None
            thwip_img = renderer.spidey_renderer.draw_thwip(1)
            assert thwip_img is not None
            print("[Spiderman] All superhero skill frames (Swing, Wall Crawl, Thwip) verified successfully!")
        elif char == "Cat":
            purr_img = renderer.cat_renderer.draw_purr(1)
            assert purr_img is not None
            walk_img = renderer.cat_renderer.draw_walk(1)
            assert walk_img is not None
            print("[Cat] Purr and Walk frames verified successfully!")
        elif char == "Puppy":
            walk_img = renderer.puppy_renderer.draw_walk(1)
            assert walk_img is not None
            print("[Puppy] Cute Puppy procedural renderer verified successfully!")
            
    print("ALL 5 CHARACTERS INITIALIZED AND TESTED SUCCESSFULLY!")
    root.destroy()

if __name__ == "__main__":
    test_character_initialization()
