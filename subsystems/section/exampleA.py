from subsystems.section.section import *

class SectionExampleA(Section):
    def render(state: State, im):
        '''Example A Area: `(  22,  22) to ( 671, 675)` : size `( 650, 654)`'''
        img = im.copy()
        rmx = state.mx - 22
        rmy = state.my - 22

        placeOver(img, displayText(f"FPS: {state.fps}", "m"), (20,20))
        placeOver(img, displayText(f"Interacting With: {state.interacting}", "m"), (20,55))
        placeOver(img, displayText(f"length of IVO: {len(state.ivos)}", "m"), (20,90))
        placeOver(img, displayText(f"Mouse Pos: ({state.mx}, {state.my})", "m"), (200,20))
        placeOver(img, displayText(f"Mouse Press: {state.mPressed}", "m", colorTXT=(100,255,100,255) if state.mPressed else (255,100,100,255)), (200,55))

        for id in state.ivos:
            if state.ivos[id][0] == "a":
                state.ivos[id][1].tick(img, state.interacting==id)

        return img    