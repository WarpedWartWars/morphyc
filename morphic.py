'''

    morphic.js

    a lively Web-GUI
    inspired by Squeak

    written by Jens Mönig
    jens@moenig.org

    Copyright (C) 2010-2021 by Jens Mönig

    This file is part of Snap!.

    Snap! is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http:##www.gnu.org/licenses/>.


    documentation contents
    ----------------------
    I. inheritance hierarchy
    II. object definition toc
    III. yet to implement
    IV. open issues
    V. browser compatibility
    VI. the big picture
    VII. programming guide
        (1) setting up a web page
            (a) single world
            (b) multiple worlds
            (c) an application
        (2) manipulating morphs
        (3) events
            (a) mouse events
            (b) context menu
            (c) dragging
            (d) dropping
            (e) keyboard events
            (f) resize event
            (g) combined mouse-keyboard events
            (h) text editing events
        (4) stepping
        (5) creating kinds of morphs
            (a) drawing the shape
            (b) determining extent and arranging submorphs
            (c) pixel-perfect pointing events
            (d) caching the shape
            (e) holes
            (f) updating
            (g) duplicating
        (6) development and user modes
        (7) turtle graphics
        (8) supporting high-resolution "retina" screens
        (9 animations
        (10) minifying morphic.js
    VIII. acknowledgements
    IX. contributors


    I. hierarchy
    -------------
    the following tree lists all constructors hierarchically,
    indentation indicating inheritance. Refer to this list to get a
    contextual overview:

    Animation
    Color
    Node
        Morph
            BlinkerMorph
                CursorMorph
            BouncerMorph*
            BoxMorph
                InspectorMorph
                MenuMorph
                MouseSensorMorph*
                SpeechBubbleMorph
            CircleBoxMorph
                SliderButtonMorph
                SliderMorph
            ColorPateMorph
                GrayPateMorph
            ColorPickerMorph
            DialMorph
            FrameMorph
                ScrollFrameMorph
                    ListMorph
                StringFieldMorph
                WorldMorph
            HandleMorph
            HandMorph
            PenMorph
            ShadowMorph
            StringMorph
            TextMorph
            TriggerMorph
                MenuItemMorph
    Point
    Rectangle


    II. toc
    -------
    the following list shows the order in which all constructors are
    defined. Use this list to locate code in this document:

    Global settings
    Global defs

    Animation
    Color
    Point
    Rectangle
    Node
    Morph
    ShadowMorph
    HandleMorph
    PenMorph
    ColorPateMorph
    GrayPateMorph
    ColorPickerMorph
    BlinkerMorph
    CursorMorph
    BoxMorph
    SpeechBubbleMorph
    DialMorph
    CircleBoxMorph
    SliderButtonMorph
    SliderMorph
    MouseSensorMorph*
    InspectorMorph
    MenuMorph
    StringMorph
    TextMorph
    TriggerMorph
    MenuItemMorph
    FrameMorph
    ScrollFrameMorph
    ListMorph
    StringFieldMorph
    BouncerMorph*
    HandMorph
    WorldMorph

    * included only for demo purposes


    III. yet to implement
    ---------------------
    - keyboard support for scroll frames and lists
    - virtual keyboard support for Android


    IV. open issues
    ----------------
    - clipboard support (copy & paste) for non-textual data


    V. browser compatibility
    ------------------------
    I have taken great care and considerable effort to make morphic.js
    runnable and appearing exactly the same on all current browsers
    available to me:

    - Firefox for Windows
    - Firefox for Mac
    - Firefox for Android
    - Chrome for Windows
    - Chrome for Mac
    - Chrome for Android
    - Safari for Windows (deprecated)
    - safari for Mac
    - Safari for iOS (mobile)
    - IE for Windows (partial support)
    - Edge for Windows
    - Opera for Windows
    - Opera for Mac


    VI. the big picture
    -------------------
    Morphic.js is compely based on Canvas and JavaScript, it is just
    Morphic, nothing else. Morphic.js is very basic and covers only the
    bare essentials:

        * a stepping mechanism (a time-sharing multiplexer for lively
          user interaction ontop of a single OS/browser thread)
        * progressive display updates (only dirty rectangles are
          redrawn at each display cycle)
        * a tree structure
        * a single World per Canvas element (although you can have
          multiple worlds in multiple Canvas elements on the same web
          page)
        * a single Hand per World (but you can support multi-touch
          events)
        * a single text entry focus per World

    In its current state morphic.js doesn't support transforms (you
    cannot rotate Morphs), but with PenMorph there already is a simple
    LOGO-like turtle that you can use to draw onto any Morph it is
    attached to. I'm planning to add special Morphs that support these
    operations later on, but not for every Morph in the system.
    Therefore these additions ("sprites" etc.) are likely to be part of
    other libraries ("microworld.js") in separate files.

    the purpose of morphic.js is to provide a malleable framework that
    will  me experiment with lively GUIs for my hobby horse, which
    is drag-and-drop, blocks based programming languages. Those things
    (BYOB4 - http:##byob.berkeley.edu) will be written using morphic.js
    as a library.


    VII. programming guide
    ----------------------
    Morphic.js provides a library for lively GUIs inside single HTML
    Canvas elements. Each such canvas element defs as a "world" in
    which other visible shapes ("morphs") can be positioned and
    manipulated, often directly and interactively by the user. Morphs
    are tree nodes and may contain any number of submorphs ("children").

    All things visible in a morphic World are morphs themselves, i.e.
    all text rendering, blinking cursors, entry fields, menus, buttons,
    sliders, windows and dialog boxes etc. are created with morphic.js
    rather than using HTML DOM elements, and as a consequence can be
    changed and adjusted by the programmer regardless of proprietary
    browser behavior.

    Each World has an - invisible - "Hand" resembling the mouse cursor
    (or the user's finger on touch screens) which handles mouse events,
    and may also have a keyboard focus to handle key events.

    The basic idea of Morphic is to continuously run display cycles and
    to incrementally update the screen by only redrawing those  World
    regions which have been "dirtied" since the last redraw. Before
    each shape is processed for redisplay it gets the chance to perform
    a "step" procedure, thus allowing for an illusion of concurrency.


    (1) setting up a web page
    -------------------------
    Setting up a web page for Morphic always involves three steps:
    adding one or more Canvas elements, defining one or more worlds,
    initializing and starting the main loop.


    (a) single world
    -----------------
    Most commonly you will want your World to fill the browsers's whole
    client area. This default situation is easiest and most straight
    forward.

    example html file:

    <!DOCTYPE html>
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html charset=UTF-8">
            <title>Morphic!</title>
            <script type="text/javascript" src="morphic.js"></script>
            <script type="text/javascript">
                world

                window.onload = def () {
                    world = WorldMorph(document.getElementById('world'))
                    world.isDevMode = True
                    loop()
                }

                def loop() {
                    requestAnimationFrame(loop)
                    world.doOneCycle()
                }
            </script>
        </head>
        <body style="margin: 0">
            <canvas id="world" tabindex="1" width="800" height="600"
                style="position: absolute"></canvas>
        </body>
    </html>

    if you use ScrollFrames or otherwise plan to support mouse wheel
    scrolling events, make sure to add the following inline-CSS
    attribute to the Canvas element:

        style="position: absolute"

    which will prevent the World to be scrolled around instead of the
    elements inside of it in some browsers.


    (b) multiple worlds
    -------------------
    If you wish to create a web page with more than one world, make
    sure to prevent each world from auto-filling the whole page and
    include it in the main loop. It's also a good idea to give each
    world its own tabindex:

    example html file:

    <!DOCTYPE html>
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html charset=UTF-8">
            <title>Morphic!</title>
            <script type="text/javascript" src="morphic.js"></script>
            <script type="text/javascript">
                var	world1, world2

                window.onload = def () {
                    disableRetinaSupport()
                    world1 = WorldMorph(
                        document.getElementById('world1'), False)
                    world2 = WorldMorph(
                        document.getElementById('world2'), False)
                    loop()
                }

                def loop() {
            requestAnimationFrame(loop)
                    world1.doOneCycle()
                    world2.doOneCycle()
                }
            </script>
        </head>
        <body>
            <p>first world:</p>
            <canvas id="world1" tabindex="1" width="600" height="400"></canvas>
            <p>second world:</p>
            <canvas id="world2" tabindex="2" width="400" height="600"></canvas>
        </body>
    </html>


    (c) an application
    -------------------
    Of course, most of the time you don't want to just plain use the
    standard Morphic World "as is" out of the box, but write your own
    application (something like Scratch!) in it. For such an
    application you'll create your own morph prototypes, perhaps
    assemble your own "window frame" and bring it all to life in a
    customized World state. the following example creates a simple
    snake-like mouse drawing game.

    example html file:

    <!DOCTYPE html>
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html charset=UTF-8">
            <title>touch me!</title>
            <script type="text/javascript" src="morphic.js"></script>
            <script type="text/javascript">
                worldCanvas, sensor

                window.onload = def () {
                    x, y, w, h

                    worldCanvas = document.getElementById('world')
                    world = WorldMorph(worldCanvas)
                    world.isDevMode = False
                    world.setColor(Color())

                    w = 100
                    h = 100

                    x = 0
                    y = 0

                    while ((y * h) < world.height()) {
                        while ((x * w) < world.width()) {
                            sensor = MouseSensorMorph()
                            sensor.setPosition(Point(x * w, y * h))
                            sensor.alpha = 0
                            sensor.setExtent(Point(w, h))
                            world.add(sensor)
                            x += 1
                        }
                        x = 0
                        y += 1
                    }
                    loop()
                }

                def loop() {
                    requestAnimationFrame(loop)
                    world.doOneCycle()
                }
            </script>
        </head>
        <body bgcolor='black' style="margin: 0">
            <canvas id="world" width="800" height="600"
                style="position: absolute"></canvas>
        </body>
    </html>

    To get an idea how you can craft your own custom morph prototypes
    I've included two examples which should give you an idea how to add
    properties, override inherited methods and use the stepping
    mechanism for "livelyness":

        BouncerMorph
        MouseSensorMorph

    For the sake of sharing a single file I've included those examples
    in morphic.js itself. Usually you'll define your additions in a
    separate file and keep morphic.js untouched.


    (2) manipulating morphs
    -----------------------
    There are many methods to programmatically manipulate morphs. Among
    the most important and common ones among all morphs are the
    following nine:

    * hide()
    * show()

    * setPosition(aPoint)
    * setExtent(aPoint)
    * setColor(aColor)

    * add(submorph)            - attaches submorph ontop
    * addBack(submorph)        - attaches submorph underneath

    * fullCopy()               - duplication
    * destroy()                - deion


    (3) events
    ----------
    All user (and system) interaction is triggered by events, which are
    passed on from the root element - the World - to its submorphs. The
    World contains a list of system (browser) events it reacts to in its

        initEventListeners()

    method. Currently there are

        - mouse
        - drop
        - keyboard
        - (window) resize

    events.

    These system events are dispatched within the morphic World by the
    World's Hand and its keyboardFocus (usually the active text
    cursor).


    (a) mouse events:
    -----------------
    The Hand dispatches the following mouse events to relevant morphs:

        mouseDownLeft
        mouseDownRight
        mouseClickLeft
        mouseClickRight
        mouseDoubleClick
        mouseEnter
        mouseLeave
        mouseEnterDragging
        mouseLeaveDragging
        mouseEnterBounds
        mouseLeaveBounds
        mouseMove
        mouseScroll

    If you wish your morph to react to any such event, simply add a
    method of the same name as the event, e.g:

        MyMorph.prototype.mouseMove = def(pos) {}

    Most of these methods have as optional parameter a Point object
    indicating the current position of the Hand inside the World's
    coordinate system. The

        mouseMove(pos, button)

    event method has an additional optional parameter indicating the
    currently pressed mouse button, which is either 'left' or 'right'.
    You can use this to  users interact with 3D environments.

    The

        mouseEnterDragging(morph)
        mouseLeaveDragging(morph)
        mouseEnterBounds(morph)
        mouseLeaveBounds(morph)

    event methods have as optional parameter the morph currently dragged by
    the Hand, if any.

    Events may be "bubbled" up a morph's owner chain by calling

        this.escalateEvent(defName, arg)

    in the event handler method's code.

    Likewise, removing the event handler method will render your morph
    passive to the event in question.


    (b) context menu:
    -----------------
    By default right-clicking (or single-finger tap-and-hold) on a morph
    also invokes its context menu (in addition to firing the
    mouseClickRight event). A morph's context menu can be customized by
    assigning a Menu instance to its

        customContextMenu

    property, or altogether suppressed by overriding its inherited

        contextMenu()

    method.


    (c) dragging:
    -------------
    Dragging a morph is initiated when the left mouse button is pressed,
    held and the mouse is moved.

    You can control whether a morph is draggable by setting its

        isDraggable

    property either to False or True. If a morph isn't draggable itself
    it will pass the pick-up request up its owner chain. This s you
    create draggable composite morphs like Windows, DialogBoxes,
    Sliders etc.

    Sometimes it is desireable to make "template" shapes which cannot be
    moved themselves, but from which instead duplicates can be peeled
    off. This is especially useful for building blocks in construction
    kits, e.g. the MIT-Scratch pate. Morphic.js s you control this
    defality by setting the

        isTemplate

    property flag to True for any morph whose "isDraggable" property is
    turned off. When dragging such a Morph the hand will instead grab
    a duplicate of the template whose "isDraggable" flag is True and
    whose "isTemplate" flag is False, in other words: a non-template.

    When creating a copy from a template, the copy's

        reactToTemplateCopy

    is invoked, if it is present.

    Dragging is indicated by adding a drop shadow to the morph in hand.
    If a morph follows the hand without displaying a drop shadow it is
    merely being moved about without changing its parent (owner morph),
    e.g. when "dragging" a morph handle to resize its owner, or when
    "dragging" a slider button.

    Right before a morph is picked up its

        selectForEdit

    and

        prepareToBeGrabbed(handMorph)

    methods are invoked, each if it is present. the optional

        selectForEdit

    if implemented, must return the object that is to be picked up.
    In addition to just returning the original object chosen by the user
    your method can also modify the target's environment and instead return
    a copy of the selected morph if, for example, you would like to implement
    a copy-on-write mechanism such as in Snap.

    Immediately after the pick-up the former parent's

        reactToGrabOf(grabbedMorph)

    method is called, again only if it exists.

    Similar to events, these  methods are optional and don't exist by
    default. For a simple example of how they can be used to adjust
    scroll bars in a scroll frame please have a look at their
    implementation in FrameMorph.


    (d) dropping:
    -------------
    Dropping is triggered when the left mouse button is either pressed
    or released while the Hand is dragging a morph.

    Dropping a morph causes it to become embedded in a owner morph.
    You can control this embedding behavior by setting the prospective
    drop target's

        acceptsDrops

    property to either True or False, or by overriding its inherited

        wantsDropOf(aMorph)

    method.

    Right before dropping a morph the designated parent's optional

        selectForEdit

    method is invoked if it is present. Again, if implemented this method
    must return the parent for the morph that is about to be dropped.
    Again, in addition to just returning the designeted drop-target
    your method can also modify its environment and instead return
    a copy of the parent if, for example, you would like to implement
    a copy-on-write mechanism such as in Snap.

    Right after a morph has been dropped its

        justDropped(handMorph)

    method is called, and its parent's

        reactToDropOf(droppedMorph, handMorph)

    method is invoked, again only if each method exists.

    Similar to events, these  methods are optional and by default are
    not present in morphs by default (watch out for inheritance,
    though!). For a simple example of how they can be used to adjust
    scroll bars in a scroll frame please have a look at their
    implementation in FrameMorph.

    Drops of image elements from outside the world canvas are dispatched as

        droppedImage(aCanvas, name)
        droppedSVG(anImage, name)

    events to interested Morphs at the mouse pointer. If you want your Morph
    to e.g. import outside images you can add the droppedImage() and / or the
    droppedSVG() methods to it. The parameter passed to the event handles is
    a offscreen canvas element representing a copy of the original image
    element which can be directly used, e.g. by assigning it to another
    Morph's cachedImage property. In the case of a dropped SVG it is an image
    element (not a canvas), which has to be rasterized onto a canvas before
    it can be used. The benefit of handling SVGs as image elements is that
    rasterization can be deferred until the destination scale is known, taking
    advantage of SVG's ability for smooth scaling. If instead SVGs are to be
    rasterized right away, you can set the

        MorphicPreferences.rasterizeSVGs

    preference to <True>. In this case dropped SVGs also trigger the
    droppedImage() event with a canvas containing a rasterized version of the
    SVG.

    The same applies to drops of audio or text files from outside the world
    canvas.

    Those are dispatched as

        droppedAudio(anAudio, name)
        droppedText(aString, name, type)

    events to interested Morphs at the mouse pointer.

    if none of the above content types can be determined, the file contents
    is dispatched as an ArrayBuffer to interested Morphs:

        droppedBinary(anArrayBuffer, name)

    In case multiple files are dropped simulateneously the events

        beginBulkDrop()
        endBulkDrop()

    are dispatched to to Morphs interested in bracketing the bulk operation,
    and the endBulkDrop() event is only signalled after the contents last file
    has been asynchronously made available.


    (e) keyboard events
    -------------------
    The World dispatches the following key events to its active
    keyboard focus:

        keypress
        keydown
        keyup

    Currently the only morphs which acts as keyboard focus are
    CursorMorph - the basic text editing widget - and MenuMorph elements.
    If you wish to add keyboard support to your morph you need to add event
    handling methods for

        processKeyPress(event)
        processKeyDown(event)
        processKeyUp(event)

    and activate them by assigning your morph to the World's

        keyboardFocus

    property.

    Note that processKeyUp() is optional and doesn't have to be present
    if your morph doesn't require it.


    (f) resize event
    ----------------
    The Window resize event is handled by the World and allows the
    World's extent to be adjusted so that it always compely fills
    the browser's visible page. You can turn off this default behavior
    by setting the World's

        useFillPage

    property to False.

    Alternatively you can also initialize the World with the
    useFillPage switch turned off from the beginning by passing the
    False value as second parameter to the World's constructor:

        world = World(aCanvas, False)

    Use this when creating a web page with multiple Worlds.

    if "useFillPage" is turned on the World dispatches an

        reactToWorldResize(newBounds)

    events to all of its children (toplevel only), allowing each to
    adjust to the World bounds by implementing a corresponding
    method, the passed argument being the World's dimensions after
    comping the resize. By default, the "reactToWorldResize" Method
    does not exist.

    Example:

    Add the following method to your Morph to  it automatically
    fill the whole World, but leave a 10 pixel border uncovered:

        MyMorph.prototype.reactToWorldResize = def (rect) {
            this.changed()
            this.bounds = rect.insetBy(10)
            this.rerender()
        }


    (g) combined mouse-keyboard events
    ----------------------------------
    Occasionally you'll want an object to react differently to a mouse
    click or to some other mouse event while the user holds down a key
    on the keyboard. Such "shift-click", "ctl-click", or "alt-click"
    events can be implemented by querying the World's

        currentKey

    property inside the def that reacts to the mouse event. This
    property stores the keyCode of the key that's currently pressed.
    Once the key is released by the user it reverts to None.


    (h) text editing events
    -----------------------
    Much of Morphic's "liveliness" comes out of allowing text elements
    (instances of either single-lined StringMorph or multi-lined TextMorph)
    to be directly manipulated and edited by users. This requires other
    objects which may have an interest in the text element's state to react
    appropriately. Therefore text elements and their manipulators emit
    a stream of events, mostly by "bubbling" them up the text element's
    owner chain. Text elements' parents are notified about the following
    events:

    Whenever the user presses a key on the keyboard while a text element
    is being edited, first a

        reactToKeystroke(event)

    is escalated up its parent chain, the "event" parameter being the
    original one received by the World.

    Whenever the input changes, by adding or removing one or more characters,
    an additional

        reactToInput(event)

    is escalated up its parent chain, the "event" parameter again being the
    original one received by the World or by the IME element.

    Note that the "reactToKeystroke" event gets triggered before the input
    changes, and thus befgore the "reactToInput" event fires.

    Once the user has comped the edit, the following events are
    dispatched:

        accept() - <enter> was pressed on a single line of text
        cancel() - <esc> was pressed on any text element

    Note that "accept" only gets triggered by single-line texte elements,
    as the <enter> key is used to insert line breaks in multi-line
    elements. Therefore, whenever a text edit is terminated by the user
    (accepted, cancelled or otherwise),

        reactToEdit(StringOrTextMorph)

    is triggered.

    If the MorphicPreference's

        useSliderForInput

    setting is turned on, a slider is popped up underneath the currently
    edited text element ting the user insert numbers out of the given
    slider range. Whenever this happens, i.e. whenever the slider is moved
    or while the slider button is pressed, a stream of

        reactToSliderEdit(StringOrTextMorph)

    events is dispatched, allowing for "Bret-Victor" style "scrubbing"
    applications.

    In addition to user-initiated events text elements also emit
    change notifications to their direct parents whenever their contents
    changes. That way complex Morphs containing text elements
    get a chance to react if something about the embedded text has been
    modified programmatically. These events are:

        layoutChanged() - sent only from instances of TextMorph
        fixLayout() - sent from instances of all Morphs, including StringMorphs

    they are different so that Morphs which contain both multi-line and
    single-line text elements can hold them apart.


    (4) stepping
    ------------
    Stepping is what makes Morphic "magical". Two properties control
    a morph's stepping behavior: the fps attribute and the step()
    method.

    By default the

        step()

    method does nothing. As you can see in the examples of BouncerMorph
    and MouseSensorMorph you can easily override this inherited method
    to suit your needs.

    By default the step() method is called once per display cycle.
    Depending on the number of actively stepping morphs and the
    complexity of your step() methods this can cause quite a strain on
    your CPU, and also result in your application behaving differently
    on slower computers than on fast ones.

    setting

        myMorph.fps

    to a number lower than the interval for the main loop s you free
    system resources (albeit at the cost of a less responsive or slower
    behavior for this particular morph).


    (5) creating kinds of morphs
    --------------------------------
    The real fun begins when you start to create kinds of morphs
    with customized shapes. Imagine, e.g. jigsaw puzzle pieces or
    musical notes.

    When you create your own morphs, you'll want to think about how to
    graphically render it, how to determine its size and whether it needs
    to arrange any other parts ("submorphs). There are also ways to specify
    its collision detection behavior and define "untouchable" regions
    ("holes").


    (a) drawing the shape
    ---------------------
    For this you have to override the default

        render(ctx)

    method.

    This method draws the morph's shape using a given 2d graphics context.
    Note that any coordinates used in the render() method must be relative
    to the morph's own position, i.e. you don't need to worry about
    translating the shape yourself.

    You can use the following template for a start:

        MyMorph.prototype.render = def(ctx) {
            ctx.fillStyle = this.color.toString()
            ctx.fillRect(0, 0, this.width(), this.height())
        }

    it renders the morph as a solid rectangle compely filling its
    area with its current color.
    
    Notice how the coordinates for the fillRect() call are relative
    to the morph's own position: The rendered rectangle's origin is always
    located at (0, 0) regardless of the morph's actual position in the World.


    (b) determining extent and arranging submorphs
    ----------------------------------------------
    If your morph also needs to determine its extent and, e.g. to
    encompass one or several other morphs, or arrange the layout of its
    submorphs, make sure to also override the default
    
        fixLayout()
    
    method.
    
    NOTE: If you need to set the morph's extent inside, in order to avoid
    infinite recursion instead of calling morph.setExtent() - which will
    in turn call morph.fixLayout() again - directly modify the morph's
    
        bounds

    property. Bounds is a rectable on which you can also use the same
    size-setters, e.g. by calling:
    
        this.bounds.setExtent()


    (c) pixel-perfect pointing events
    ---------------------------------
    In case your morph needs to support pixel-perfect collision detection
    with other morphs or pointing devices such as the mouse or a stylus you
    can set the inherited attribute
    
        isFreeForm = bool
    
    to "True" (default is "False"). This makes sense the more your morph's
    visual shape diverges from a rectangle. For example, if you create a
    circular filled morph the default setting will register mouse-events
    anywhere within its bounding box, e.g. also in the transparent parts
    between the bounding box's corners outside of the circle's bounds.
    Instead you can specify your irregulary shaped morph to only register
    pointing events (mouse and touch) on solid, non-transparent parts.

    Notice, however, that such pixel-perfect collision detection might
    strain processing resources, especially if applied liberally.

    In order to mitigate unfavorable processor loads for pixel-perfect
    collision deteciton of irregularly shaped morphs there are two strategies
    to consider: Caching the shape and specifying "untouchable" regions.


    (d) caching the shape
    ---------------------
    In case of pixel-perfect free-form collision detection it makes sense to
    cache your morph's current shape, so it doesn't have to be re-drawn onto a
    Canvas element every time the mouse moves over its bounding box.
    For this you can set then inherited
    
        isCachingImage = bool
        
    attribute to "True" instead of the default "False" value. This will
    significantly speed up collision detection and smoothen animations that
    continuously perform collision detection. However, it will also consume
    more memory. Therefore it's best to use this setting with caution.
    
    Snap! caches the shapes of sprites but not those of blocks. Instead it
    manages the insides of C- and E-shaped blocks through the morphic "holes"
    mechanism.


    (e) holes
    ---------
    An alternative albeit not as precise and general way for handling
    irregularly shaped morphs with "untouchable" regions is to specify a set
    of rectangular areas in which pointing events (mouse or touch) are not
    registered.

    By default the inherited
    
        holes = []

    property is an empty array. You can add one or more morphic Rectangle
    objects to this list, representing regions, in which occurring events will
    instead be passed on to the morph underneath.
    
    Note that, same with the render() method, the coordinates of these
    rectangular holes must be specified relative to your morph's position.

    If you specify holes you might find the need to adjust their layout
    depending on the layout of your morph. To accomplish this you can override
    the inherited
    
        fixHolesLayout()

    method.


    (f) updating
    ------------
    One way for morphs to become alive is form them to literally "morph" their
    shape depending on whicher contest you wish them to react to. For example,
    you might want the user to interactively draw a shape using their fingers
    on a touch screen device, or you want the user to be able to "pinch" or
    otherwise distort a shape interactively. In all of these situations you'll
    want your morph to frequently rerender its shape.
    
    You can accomplish this, by calling

        rerender()

    after every change to your morph's appearance that requires rerendering.
    
    Such changes are usually only happening when the morph's dimensions or
    other visual properties - such as its color - changes.


    (g) duplicating
    ---------------
    If your morph stores or references to other morphs outside of
    the submorph tree in other properties, be sure to also override the
    default

        updateReferences()

    method if you want it to support duplication.


    (6) development and user modes
    ------------------------------
    When working with Squeak on Scratch or BYOB among the features I
    like the best and use the most is inspecting what's going on in
    the World while it is up and running. That's what development mode
    is for (you could also call it debug mode). In essence development
    mode controls which context menu shows up. In user mode right
    clicking (or double finger tapping) a morph invokes its

        customContextMenu

    property, whereas in development mode only the general

        developersMenu()

    method is called and the resulting menu invoked. The developers'
    menu features Gui-Builder-wise defality to directly inspect,
    take apart, reassamble and otherwise manipulate morphs and their
    contents.

    Instead of using the "customContextMenu" property you can also
    assign a more dynamic contextMenu by overriding the general

        userMenu()

    method with a customized menu constructor. The difference between
    the customContextMenu property and the userMenu() method is that
    the former is also present in development mode and overrides the
    developersMenu() result. For an example of how to use the
    customContextMenu property have a look at TextMorph's evaluation
    menu, which is used for the Inspector's evaluation pane.

    When in development mode you can inspect every Morph's properties
    with the inspector, including all of its methods. The inspector
    also s you add, remove and rename properties, and even edit
    their values at runtime. Like in a Smalltalk environment the inspect
    features an evaluation pane into which you can type in arbitrary
    JavaScript code and evaluate it in the context of the inspectee.

    Use switching between user and development modes while you are
    developing an application and disable switching to development once
    you're done and deploying, because generally you don't want to
    confuse end-users with inspectors and meta-level stuff.


    (7) turtle graphics
    -------------------

    The basic Morphic kernel features a simple LOGO turtle constructor
    called

        PenMorph

    which you can use to draw onto its parent Morph. By default every
    Morph in the system (including the World) is able to act as turtle
    canvas and can display pen trails. Pen trails will be lost whenever
    the trails morph (the pen's parent) performs a "render()"
    operation. If you want to create your own pen trails canvas, you
    may wish to modify its

        penTrails()

    property, so that it keeps a separate offscreen canvas for pen
    trails (and doesn't loose these on redraw).

    the following properties of PenMorph are relevant for turtle
    graphics:

        color       - a Color
        size        - line width of pen trails
        heading     - degrees
        isDown      - drawing state

    the following commands can be used to actually draw something:

        up()        - lift the pen up, further movements leave no trails
        down()      - set down, further movements leave trails
        clear()     - remove all trails from the current parent
        forward(n)  - move n steps in the current direction (heading)
        turn(n)     - turn right n degrees

    Turtle graphics can best be explored interactively by creating a
    PenMorph object and by manipulating it with the inspector
    widget.

    NOTE: PenMorph has a special optimization for recursive operations
    called

        warp(def)

    You can significantly speed up recursive ops and increase the depth
    of recursion that's displayable by wrapping WARP around your
    recursive def call:

    example:

        myPen.warp(def () {
            myPen.tree(12, 120, 20)
        })

    will be much faster than just invoking the tree def, because it
    prevents the parent's parent from keeping track of every single line
    segment and instead redraws the outcome in a single pass.


    (8) supporting high-resolution "retina" screens
    -----------------------------------------------
    By default retina support gets installed when Morphic.js loads. There
    are two global defs that  you test for retina availability:

        isRetinaSupported() - Bool, answers if retina support is available
        isRetinaEnabled()   - Bool, answers if currently in retina mode

    and two more defs that  you control retina support if it is
    available:

        enableRetinaSupport()
        disableRetinaSupport()

    Both of these internally test whether retina is available, so they are
    safe to call directly. For an example how to make retina support
    user-specifiable refer to

        Snap! >> guis.js >> toggleRetina()

    Even when in retina mode it often makes sense to use normal-resolution
    canvasses for simple shapes in order to save system resources and
    optimize performance. Examples are costumes and backgrounds in Snap.
    In Morphic you can create canvas elements using

        newCanvas(extentPoint [, nonRetinaFlag])

    If retina support is enabled such canvasses will automatically be
    high-resolution canvasses, unless the newCanvas() def is given an
    otherwise optional second Boolean <True> argument that explicitly makes
    it a non-retina canvas.

    Not the whole canvas API is supported by Morphic's retina utilities.
    Especially if your code uses putImageData() you will want to "downgrade"
    a target high-resolution canvas to a normal-resolution ("non-retina")
    one before using

        normalizeCanvas(aCanvas [, copyFlag])

    This will change the target canvas' resolution in place (!). If you
    pass in the optional second Boolean <True> flag the def returns
    a non-retina copy and leaves the target canvas unchanged. An example
    of this normalize mechanism is converting the penTrails layer of Snap's
    stage (high-resolution) into a sprite-costume (normal resolution).


    (9) animations
    ---------------
    Animations handle gradual transitions between one state and another over a
    period of time. Transition effects can be specified using easing defs.
    An easing def maps a fraction of the transition time to a fraction of
    the state delta. This way accelerating / decelerating and bouncing sliding
    effects can be accomplished.

    Animations are generic and not limited to motion, i.e. they can also handle
    other transitions such as color changes, transparency fadings, growing,
    shrinking, turning etc.

    Animations need to be stepped by a scheduler, e. g. an interval def.
    In Morphic the preferred way to run an animation is to register it with
    the World by adding it to the World's animation queue. The World steps each
    registered animation once per display cycle independently of the Morphic
    stepping mechanism.

    For an example how to use animations look at how the Morph's methods

        glideTo()
        fadeTo()

    and

        slideBackTo()

    are implemented.


    (10) minifying morphic.js
    -------------------------
    Coming from Smalltalk and being a Squeaker at heart I am a huge fan
    of browsing the code itself to make sense of it. Therefore I have
    included this documentation and (too little) inline comments so all
    you need to get going is this very file.

    Nowadays with live streaming HD video even on mobile phones 250 KB
    shouldn't be a big strain on bandwith, still minifying and even
    compressing morphic.js down do about 100 KB may sometimes improve
    performance in production use.

    Being an attorney-at-law myself you programmer folk keep harassing
    me with rabulistic nitpickings about free software licenses. I'm
    releasing morphic.js under an AGPL license. Therefore please make
    sure to adhere to that license in any minified or compressed version.


    VIII. acknowledgements
    ----------------------
    The original Morphic was designed and written by Randy Smith and
    John Maloney for the SELF programming language, and later ported to
    Squeak (Smalltalk) by John Maloney and Dan Ingalls, who has also
    ported it to JavaScript (the Lively Kernel), once again setting
    a "Gold Standard" for self sustaining systems which morphic.js
    cannot and does not aspire to meet.

    This Morphic implementation for JavaScript is not a direct port of
    Squeak's Morphic, but still many individual defs have been
    ported almost literally from Squeak, sometimes even including their
    comments, e.g. the morph duplication mechanism fullCopy(). Squeak
    has been a treasure trove, and if morphic.js looks, feels and
    smells a lot like Squeak, I'll take it as a compliment.

    Evelyn Eastmond has inspired and encouraged me with her wonderful
    implementation of DesignBlocksJS. Thanks for sharing code, ideas
    and enthusiasm for programming.

    John Maloney has been my mentor and my source of inspiration for
    these Morphic experiments. Thanks for the critique, the suggestions
    and explanations for all things Morphic and for being my all time
    programming hero.

    I have originally written morphic.js in Florian Balmer's Notepad2
    editor for Windows, later switched to Apple's Dashcode and later
    still to Apple's Xcode. I've also come to depend on both Douglas
    Crockford's JSLint and later the JSHint project, as well as on
    Mozilla's Firebug and Google's Chrome to get it right.


    IX. contributors
    ----------------------
    Joe Otto found and fixed many early bugs and taught me some tricks.
    Nathan Dinsmore contributed mouse wheel scrolling, cached
    background texture handling, countless bug fixes and optimizations.
    Ian Reynolds contributed backspace key handling for Chrome.
    Davide Della Casa contributed performance optimizations for Firefox.
    Jason N (@cyderize) contributed native copy & paste for text editing.
    Bartosz Leper contributed retina display support.
    Zhenlei Jia and Dariusz Dorożalski pioneered IME text editing.
    Bernat Romagosa contributed to text editing and to the core design.
    Michael Ball found and fixed a longstanding scrolling bug.
    Brian Harvey contributed to the design and implementation of submenus.
    Ken Kahn contributed to Chinese keboard entry and Android support.
    Brian Broll contributed clickable URLs in text elements and many bugfixes.

    - Jens Mönig
'''

## Global settings #####################################################

'''global window, HTMLCanvasElement, FileReader, Audio, FileList, Map'''

morphicVersion = '2021-July-09'
modules = {} ## keep track of additional loaded modules
useBlurredShadows = True

ZERO = Point()
BLACK = Color()
WHITE = Color(255, 255, 255)
CLEAR = Color(0, 0, 0, 0)

standardSettings = {
    'minimumFontHeight': getMinimumFontHeight(), ## browser settings
    'globalFontFamily': '',
    'menuFontName': 'sans-serif',
    'menuFontSize': 12,
    'bubbleHelpFontSize': 10,
    'prompterFontName': 'sans-serif',
    'prompterFontSize': 12,
    'prompterSliderSize': 10,
    'handleSize': 15,
    'scrollBarSize': 9, ## was 12,
    'mouseScrollAmount': 40,
    'useSliderForInput': False,
    'isTouchDevice': False, ## turned on by touch events, don't set
    'rasterizeSVGs': False,
    'isFlat': False,
    'grabThreshold': 5,
    'showHoles': False
}

touchScreenSettings = {
    'minimumFontHeight': standardSettings.minimumFontHeight,
    'globalFontFamily': '',
    'menuFontName': 'sans-serif',
    'menuFontSize': 24,
    'bubbleHelpFontSize': 18,
    'prompterFontName': 'sans-serif',
    'prompterFontSize': 24,
    'prompterSliderSize': 20,
    'handleSize': 26,
    'scrollBarSize': 24,
    'mouseScrollAmount': 40,
    'useSliderForInput': False,
    'isTouchDevice': True,
    'rasterizeSVGs': False,
    'isFlat': False,
    'grabThreshold': 5,
    'showHoles': False
}

MorphicPreferences = standardSettings

## first, try enabling support for retina displays - can be turned off later

'''
    Support for retina displays has been pioneered and contributed by
    Bartosz Leper.

    NOTE: this will make changes to the HTMLCanvasElement that - mostly -
    make Morphic usable on retina displays in very high resolution mode
    with crisp fonts and clear fine lines without you (the programmer)
    needing to know any specifics, provided both the display and the browser
    support these (Safari currently doesn't), otherwise these utilities will
    not be installed.
    If you don't want your Morphic application to support retina resolutions
    you don't have to edit this morphic.js file to comment out the next line
    of code, instead you can simply call

        disableRetinaSupport()

    before you create your World(s) in the html page. Disabling retina
    support also will simply do nothing if retina support is not possible
    or already disabled, so it's equally safe to call.

    For an example how to make retina support user-specifiable refer to
    Snap! >> gui.js >> toggleRetina()
'''

enableRetinaSupport()

## Global defs ####################################################

def nop():
    ## do explicitly nothing
    return None

def localize(string):
    ## override this function with custom localizations
    return string

def isNil(thing):
    return thing is None

def contains(list, element):
    ## answer True if element is a member of list
    return element in list

def detect(list, predicate):
    ## answer the first element of list for which predicate evaluates
    ## True, otherwise answer None
    for item in list:
        if predicate(item):
            return item
    return None

def sizeOf(object):
    ## answer the number of own properties
    return len(dir(object))

def isString(target):
    return isinstance(target, str)

def isObject(target):
    return target is not None

import math

def radians(degrees):
    return degrees * math.pi / 180

def degrees(radians):
    return radians * 180 / math.pi

def fontHeight(height):
    minHeight = max(height, MorphicPreferences.minimumFontHeight)
    return minHeight * 1.2 ## assuming 1/5 font size for ascenders

import re

def isWordChar(aCharacter):
    ## can't use \b or \w because they ignore diacritics
    return bool(re.match(r'[A-Za-zÀ-ÿ0-9]', aCharacter))

def isURLChar(aCharacter):
    return bool(re.match(r'[A-z0-9./:?&_+%-]', aCharacter))

def isURL(text):
    return bool(re.match('^https?://', text))

########################################################################
########################################################################
########################################################################
########################################################################
########################################################################

def newCanvas(extentPoint, nonRetina, recycleMe) {
    ## answer a empty instance of Canvas, don't display anywhere
    ## nonRetina - optional Boolean "False"
    ## by default retina support is automatic
    ## optional existing canvas to be used again, unless it is marked as
    ## being shared among Morphs (dataset property "morphicShare")
    canvas, ext
    nonRetina = nonRetina || False
    ext = (extentPoint ||
            (recycleMe ? Point(recycleMe.width, recycleMe.height)
                : Point(0, 0))).ceil()
    if (recycleMe &&
            !recycleMe.dataset.morphicShare &&
            (recycleMe.isRetinaEnabled || False) != nonRetina &&
            ext.x == recycleMe.width && ext.y == recycleMe.height
    ) {
        canvas = recycleMe
        canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height)
        return canvas
    } else {
        canvas = document.createElement('canvas')
        canvas.width = ext.x
        canvas.height = ext.y
    }
    if (nonRetina && canvas.isRetinaEnabled) {
        canvas.isRetinaEnabled = False
    }
    return canvas
}

def copyCanvas(aCanvas) {
    ## answer a deep copy of a canvas element respecting its retina status
    c
    if (aCanvas && aCanvas.width && aCanvas.height) {
        c = newCanvas(
            Point(aCanvas.width, aCanvas.height),
            !aCanvas.isRetinaEnabled
        )
        c.getContext("2d").drawImage(aCanvas, 0, 0)
        return c
    }
    return aCanvas
}

def getMinimumFontHeight() {
    ## answer the height of the smallest font renderable in pixels
    str = 'I',
        size = 50,
        canvas = document.createElement('canvas'),
        ctx,
        maxX,
        data,
        x,
        y
    canvas.width = size
    canvas.height = size
    ctx = canvas.getContext('2d')
    ctx.font = '1px serif'
    maxX = ctx.measureText(str).width
    ctx.fillStyle = 'black'
    ctx.textBaseline = 'bottom'
    ctx.fillText(str, 0, size)
    for (y = 0 y < size y += 1) {
        for (x = 0 x < maxX x += 1) {
            data = ctx.getImageData(x, y, 1, 1)
            if (data.data[3] != 0) {
                return size - y + 1
            }
        }
    }
    return 0
}

def getDocumentPositionOf(aDOMelement) {
    ## answer the relative coordinates of a DOM element in the viewport
    rect = aDOMelement.getBoundingClientRect(),
    scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
    scrollTop = window.pageYOffset || document.documentElement.scrollTop
    return {x: rect.left + scrollLeft, y:rect.top + scrollTop}
}

def copy(target) {
    ## answer a shallow copy of target
    value, c, property, keys, l, i
    if (typeof target != 'object') {
        return target
    }
    value = target.valueOf()
    if (target != value) {
        return target.constructor(value)
    }
    if (target instanceof target.constructor &&
            target.constructor != Object) {
        c = Object.create(target.constructor.prototype)
        keys = Object.keys(target)
        for (l = keys.length, i = 0 i < l i += 1) {
            property = keys[i]
            if (target[property] instanceof HTMLCanvasElement) {
                ## tag canvas elements as being shared,
                ## so the next time when rerendering a Morph
                ## instead of recycling the shared canvas a
                ## unshared one get created
                ## see newCanvas() def
                target[property].dataset.morphicShare = 'True'
            }
            c[property] = target[property]
        }
    } else {
        c = {}
        for (property in target) {
            c[property] = target[property]
        }
    }
    return c
}

## Retina Display Support ##############################################

'''
    By default retina support gets installed when Morphic.js loads. There
    are two global defs that  you test for retina availability:

        isRetinaSupported() - Boolean, whether retina support is available
        isRetinaEnabled()   - Boolean, whether currently in retina mode

    and two more defs that  you control retina support if it is
    available:

        enableRetinaSupport()
        disableRetinaSupport()

    Both of these internally test whether retina is available, so they are
    safe to call directly.

    Even when in retina mode it often makes sense to use non-high-resolution
    canvasses for simple shapes in order to save system resources and
    optimize performance. Examples are costumes and backgrounds in Snap.
    In Morphic you can create canvas elements using

        newCanvas(extentPoint [, nonRetinaFlag])

    If retina support is enabled such canvasses will automatically be
    high-resolution canvasses, unless the newCanvas() def is given an
    otherwise optional second Boolean <True> argument that explicitly makes
    it a non-retina canvas.

    Not the whole canvas API is supported by Morphic's retina utilities.
    Especially if your code uses putImageData() you will want to "downgrade"
    a target high-resolution canvas to a normal-resolution ("non-retina")
    one before using

        normalizeCanvas(aCanvas [, copyFlag])

    This will change the target canvas' resolution in place (!). If you
    pass in the optional second Boolean <True> flag the def returns
    a non-retina copy and leaves the target canvas unchanged. An example
    of this normalize mechanism is converting the penTrails layer of Snap's
    stage (high-resolution) into a sprite-costume (normal resolution).
'''

def enableRetinaSupport() {
'''
    === contributed by Bartosz Leper ===

    This installs a series of utilities that allow using Canvas the same way
    on retina and non-retina displays. If the display is a retina one, the
    underlying dimensions of the Canvas elements are doubled, but this will
    be transparent to the code that uses Canvas. All dimensions read or
    written to the Canvas element will be scaled appropriately.

    NOTE: This implementation is not exhaustive it only implements what is
    needed by the Snap! UI.

    [Jens]: like all other retina screen support implementations I've seen
    Bartosz's patch also does not address putImageData() compatibility when
    mixing retina-enabled and non-retina canvasses. If you need to manipulate
    pixels in such mixed canvasses, make sure to "downgrade" them all using
    normalizeCanvas() below.
'''

    ## Get the window's pixel ratio for canvas elements.
    ## See: http:##www.html5rocks.com/en/tutorials/canvas/hidpi/
    ctx = document.createElement("canvas").getContext("2d"),
        backingStorePixelRatio = ctx.webkitBackingStorePixelRatio ||
            ctx.mozBackingStorePixelRatio ||
            ctx.msBackingStorePixelRatio ||
            ctx.oBackingStorePixelRatio ||
            ctx.backingStorePixelRatio || 1,

    ## Unfortunately, it's really hard to make this work well when changing
    ## zoom level, so 's leave it like this right now, and stick to
    ## whatever the ratio was in the beginning.

        ## originalDevicePixelRatio = window.devicePixelRatio,

    ## [Jens]: As of summer 2016 non-integer devicePixelRatios lead to
    ## artifacts when blitting images onto canvas elements in all browsers
    ## except Chrome, especially Firefox, Edge, IE (Safari doesn't even
    ## support retina mode as implemented here).
    ## therefore - to ensure crisp fonts - use the ceiling of whatever
    ## the devicePixelRatio is. This needs more memory, but looks nicer.

        originalDevicePixelRatio = math.ceil(window.devicePixelRatio),

        canvasProto = HTMLCanvasElement.prototype,
        contextProto = CanvasRenderingContext2D.prototype,

    ## [Jens]: keep track of original properties in a dictionary
    ## so they can be iterated over and restored
        uber = {
            drawImage: contextProto.drawImage,
            getImageData: contextProto.getImageData,

            width: Object.getOwnPropertyDescriptor(
                canvasProto,
                'width'
            ),
            height: Object.getOwnPropertyDescriptor(
                canvasProto,
                'height'
            ),
            shadowOffsetX: Object.getOwnPropertyDescriptor(
                contextProto,
                'shadowOffsetX'
            ),
            shadowOffsetY: Object.getOwnPropertyDescriptor(
                contextProto,
                'shadowOffsetY'
            ),
            shadowBlur: Object.getOwnPropertyDescriptor(
                contextProto,
                'shadowBlur'
            )
        }

    ## [Jens]: only install retina utilities if the display supports them
    if (backingStorePixelRatio == originalDevicePixelRatio) {return }
    ## [Jens]: check whether properties can be overridden, needed for Safari
    if (Object.keys(uber).some(any => {
        prop = uber[any]
        return prop.hasOwnProperty('configurable') && (!prop.configurable)
    })) {return }

    def getPixelRatio(imageSource) {
        return imageSource.isRetinaEnabled ?
            (originalDevicePixelRatio || 1) / backingStorePixelRatio : 1
    }

    canvasProto._isRetinaEnabled = True
    ## [Jens]: remember the original non-retina properties,
    ## so they can be restored again
    canvasProto._bak = uber

    Object.defineProperty(canvasProto, 'isRetinaEnabled', {
        get: def() {
            return this._isRetinaEnabled
        },
        set: def(enabled) {
            prevPixelRatio = getPixelRatio(this),
                prevWidth = this.width,
                prevHeight = this.height

            this._isRetinaEnabled = enabled
            if (getPixelRatio(this) != prevPixelRatio) {
                this.width = prevWidth
                this.height = prevHeight
            }
        },
        configurable: True ## [Jens]: allow to be deed an reconfigured
    })

    Object.defineProperty(canvasProto, 'width', {
        get: def() {
            return uber.width.get.call(this) / getPixelRatio(this)
        },
        set: def(width) {
            try { ## workaround one of FF's dreaded NS_ERROR_FAILURE bugs
                ## this should be taken out as soon as FF gets fixed again
                pixelRatio = getPixelRatio(this),
                    context
                uber.width.set.call(this, width * pixelRatio)
                context = this.getContext('2d')
                /*
                context.restore()
                context.save()
                */
                context.scale(pixelRatio, pixelRatio)
            } catch (err) {
                console.log('Retina Display Support Problem', err)
                uber.width.set.call(this, width)
            }
        }
    })

    Object.defineProperty(canvasProto, 'height', {
        get: def() {
            return uber.height.get.call(this) / getPixelRatio(this)
        },
        set: def(height) {
            pixelRatio = getPixelRatio(this),
                context
            uber.height.set.call(this, height * pixelRatio)
            context = this.getContext('2d')
            /*
            context.restore()
            context.save()
            */
            context.scale(pixelRatio, pixelRatio)
        }
    })

    contextProto.drawImage = def(image) {
        pixelRatio = getPixelRatio(image),
            sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight

        ## Different signatures of drawImage() method have different
        ## parameter assignments.
        switch (arguments.length) {
            case 9:
                sx = arguments[1]
                sy = arguments[2]
                sWidth = arguments[3]
                sHeight = arguments[4]
                dx = arguments[5]
                dy = arguments[6]
                dWidth = arguments[7]
                dHeight = arguments[8]
                break

            case 5:
                sx = 0
                sy = 0
                sWidth = image.width
                sHeight = image.height
                dx = arguments[1]
                dy = arguments[2]
                dWidth = arguments[3]
                dHeight = arguments[4]
                break

            case 3:
                sx = 0
                sy = 0
                sWidth = image.width
                sHeight = image.height
                dx = arguments[1]
                dy = arguments[2]
                dWidth = image.width
                dHeight = image.height
                break

            default:
                throw Error('Called drawImage() with ' + arguments.length +
                        ' arguments')
        }
        uber.drawImage.call(
                this, image,
                sx * pixelRatio, sy * pixelRatio,
                sWidth * pixelRatio, sHeight * pixelRatio,
                dx, dy,
                dWidth, dHeight)
    }

    contextProto.getImageData = def(sx, sy, sw, sh) {
        pixelRatio = getPixelRatio(this.canvas)
        return uber.getImageData.call(
                this,
                sx * pixelRatio, sy * pixelRatio,
                sw * pixelRatio, sh * pixelRatio)
    }

    Object.defineProperty(contextProto, 'shadowOffsetX', {
        get: def() {
            return uber.shadowOffsetX.get.call(this) /
                getPixelRatio(this.canvas)
        },
        set: def(offset) {
            pixelRatio = getPixelRatio(this.canvas)
            uber.shadowOffsetX.set.call(this, offset * pixelRatio)
        }
    })

    Object.defineProperty(contextProto, 'shadowOffsetY', {
        get: def() {
            return uber.shadowOffsetY.get.call(this) /
                getPixelRatio(this.canvas)
        },
        set: def(offset) {
            pixelRatio = getPixelRatio(this.canvas)
            uber.shadowOffsetY.set.call(this, offset * pixelRatio)
        }
    })

    Object.defineProperty(contextProto, 'shadowBlur', {
        get: def() {
            return uber.shadowBlur.get.call(this) /
                getPixelRatio(this.canvas)
        },
        set: def(blur) {
            pixelRatio = getPixelRatio(this.canvas)
            uber.shadowBlur.set.call(this, blur * pixelRatio)
        }
    })
}

def isRetinaSupported () {
    ctx = document.createElement("canvas").getContext("2d"),
        backingStorePixelRatio = ctx.webkitBackingStorePixelRatio ||
            ctx.mozBackingStorePixelRatio ||
            ctx.msBackingStorePixelRatio ||
            ctx.oBackingStorePixelRatio ||
            ctx.backingStorePixelRatio || 1,
        canvasProto = HTMLCanvasElement.prototype,
        contextProto = CanvasRenderingContext2D.prototype,
        uber = {
            drawImage: contextProto.drawImage,
            getImageData: contextProto.getImageData,

            width: Object.getOwnPropertyDescriptor(
                canvasProto,
                'width'
            ),
            height: Object.getOwnPropertyDescriptor(
                canvasProto,
                'height'
            ),
            shadowOffsetX: Object.getOwnPropertyDescriptor(
                contextProto,
                'shadowOffsetX'
            ),
            shadowOffsetY: Object.getOwnPropertyDescriptor(
                contextProto,
                'shadowOffsetY'
            ),
            shadowBlur: Object.getOwnPropertyDescriptor(
                contextProto,
                'shadowBlur'
            )
        }
    return backingStorePixelRatio != window.devicePixelRatio &&
        !(Object.keys(uber).some(any => {
            prop = uber[any]
            return prop.hasOwnProperty('configurable') && (!prop.configurable)
        })
    )
}

def isRetinaEnabled () {
    return HTMLCanvasElement.prototype.hasOwnProperty('_isRetinaEnabled')
}

def disableRetinaSupport() {
    ## uninstalls Retina utilities. Make sure to re-create every Canvas
    ## element afterwards
    canvasProto, contextProto, uber
    if (!isRetinaEnabled()) {return }
    canvasProto = HTMLCanvasElement.prototype
    contextProto = CanvasRenderingContext2D.prototype
    uber = canvasProto._bak
    Object.defineProperty(canvasProto, 'width', uber.width)
    Object.defineProperty(canvasProto, 'height', uber.height)
    contextProto.drawImage = uber.drawImage
    contextProto.getImageData = uber.getImageData
    Object.defineProperty(contextProto, 'shadowOffsetX', uber.shadowOffsetX)
    Object.defineProperty(contextProto, 'shadowOffsetY', uber.shadowOffsetY)
    Object.defineProperty(contextProto, 'shadowBlur', uber.shadowBlur)
    dee canvasProto._isRetinaEnabled
    dee canvasProto.isRetinaEnabled
    dee canvasProto._bak
}

def normalizeCanvas(aCanvas, getCopy) {
    ## make sure aCanvas is non-retina, otherwise convert it in place (!)
    ## or answer a normalized copy if the "getCopy" flag is <True>
    cpy
    if (!aCanvas.isRetinaEnabled) {return aCanvas }
    cpy = newCanvas(Point(aCanvas.width, aCanvas.height), True)
    cpy.getContext('2d').drawImage(aCanvas, 0, 0)
    if (getCopy) {return cpy }
    aCanvas.isRetinaEnabled = False
    aCanvas.width = cpy.width
    aCanvas.height = cpy.height
    aCanvas.getContext('2d').drawImage(cpy, 0, 0)
    return aCanvas
}

## Animations ##############################################################

/*
    Animations handle gradual transitions between one state and another over a
    period of time. Transition effects can be specified using easing defs.
    An easing def maps a fraction of the transition time to a fraction of
    the state delta. This way accelerating / decelerating and bouncing sliding
    effects can be accomplished.

    Animations are generic and not limited to motion, i.e. they can also handle
    other transitions such as color changes, transparency fadings, growing,
    shrinking, turning etc.

    Animations need to be stepped by a scheduler, e. g. an interval def.
    In Morphic the preferred way to run an animation is to register it with
    the World by adding it to the World's animation queue. The World steps each
    registered animation once per display cycle independently of the Morphic
    stepping mechanism.

    For an example how to use animations look at how the Morph's methods

        glideTo()
        fadeTo()

    and

        slideBackTo()

    are implemented.
*/

## Animation instance creation:

def Animation(setter, getter, delta, duration, easing, onCompe) {
    this.setter = setter ## def
    this.getter = getter ## def
    this.delta = delta || 0 ## number
    this.duration = duration || 0 ## milliseconds
    this.easing = isString(easing) ? ## string or def
            this.easings[easing] || this.easings.sinusoidal
                : easing || this.easings.sinusoidal
    this.onCompe = onCompe || None ## optional callback
    this.endTime = None
    this.destination = None
    this.isActive = False
    this.start()
}

Animation.prototype.easings = {
    ## dictionary of a few pre-defined easing defs used to transition
    ## two states

    ## ease both in and out:
    linear: t => t,
    sinusoidal: t => 1 - math.cos(radians(t * 90)),
    quadratic: t => t < 0.5 ? 2 * t * t : ((4 - (2 * t)) * t) - 1,
    cubic: t => {
        return t < 0.5 ?
            4 * t * t * t
                : ((t - 1) * ((2 * t) - 2) * ((2 * t) - 2)) + 1
    },
    elastic: t => {
        return (t -= 0.5) < 0 ?
            (0.01 + 0.01 / t) * math.sin(50 * t)
                : (0.02 - 0.01 / t) * math.sin(50 * t) + 1
    },

    ## ease in only:
    sine_in: t => 1 - math.sin(radians(90 + (t * 90))),
    quad_in: t => t * t,
    cubic_in: t => t * t * t,
    elastic_in: t => (0.04 - 0.04 / t) * math.sin(25 * t) + 1,

    ## ease out only:
    sine_out: t => math.sin(radians(t * 90)),
    quad_out: t => t * (2 - t),
    elastic_out: t => 0.04 * t / (--t) * math.sin(25 * t)
}

Animation.prototype.start = def () {
    ## (re-) activate the animation, e.g. if is has previously comped,
    ## make sure to plug it into something that repeatedly triggers step(),
    ## e.g. the World's animations queue
    this.endTime = Date.now() + this.duration
    this.destination = this.getter.call(this) + this.delta
    this.isActive = True
}

Animation.prototype.step = def () {
    if (!this.isActive) {return }
    now = Date.now()
    if (now > this.endTime) {
        this.setter(this.destination)
        this.isActive = False
        if (this.onCompe) {this.onCompe() }
    } else {
        this.setter(
            this.destination -
                (this.delta * this.easing((this.endTime - now) / this.duration))
        )
    }
}

## Colors ##############################################################

## Color instance creation:

def Color(r, g, b, a) {
    ## all values are optional, just (r, g, b) is fine
    this.r = r || 0
    this.g = g || 0
    this.b = b || 0
    this.a = a || ((a == 0) ? 0 : 1)
}

## Color string representation: e.g. 'rgba(255,165,0,1)'

Color.prototype.toString = def () {
    return 'rgba(' +
        math.round(this.r) + ',' +
        math.round(this.g) + ',' +
        math.round(this.b) + ',' +
        this.a + ')'
}

Color.prototype.toRGBstring = def () {
    return 'rgb(' +
        math.round(this.r) + ',' +
        math.round(this.g) + ',' +
        math.round(this.b) + ')'
}

Color.fromString = def (aString) {
    ## I parse rgb/rgba strings into a Color object
    components = aString.split(/[\(),]/).slice(1,5)
    return Color(components[0], components[1], components[2], components[3])
}

## Color copying:

Color.prototype.copy = def () {
    return Color(
        this.r,
        this.g,
        this.b,
        this.a
    )
}

## Color comparison:

Color.prototype.eq = def (aColor, observeAlpha) {
    ## ==
    return aColor &&
        this.r == aColor.r &&
        this.g == aColor.g &&
        this.b == aColor.b &&
        (observeAlpha ? this.a == aColor.a : True)
}

Color.prototype.isCloseTo = def (aColor, observeAlpha, tolerance) {
    ## experimental - answer whether a color is "close" to another one by
    ## a given percentage. tolerance is the percentage by which each color
    ## channel may diverge, alpha needs to be the exact same unless ignored
    thres = 2.55 * (tolerance || 10)

    def dist(a, b) {
        diff = a - b
        return diff < 0 ? 255 + diff : diff
    }

    return aColor &&
        dist(this.r, aColor.r) < thres &&
        dist(this.g, aColor.g) < thres &&
        dist(this.b, aColor.b) < thres &&
        (observeAlpha ? this.a == aColor.a : True)
}

## Color conversion (hsv):

Color.prototype.hsv = def () {
    ## ignore alpha
    rr = this.r / 255
    gg = this.g / 255
    bb = this.b / 255
    max_ = max(rr, gg, bb)
    min_ = min(rr, gg, bb)
    h = max_
    s = max_
    v = max_
    d = max_ - min_
    s = max_ == 0 ? 0 : d / max_
    if (max_ == min_) {
        h = 0
    } else {
        if rr == max_:
            h = (gg - bb) / d + (gg < bb ? 6 : 0)
        elif gg == max_:
            h = (bb - rr) / d + 2
        elif bb == max_:
            h = (rr - gg) / d + 4
        }
        h /= 6
    }
    return [h, s, v]
}

Color.prototype.set_hsv = def (h, s, v) {
    ## ignore alpha, h, s and v are to be within [0, 1]
    i, f, p, q, t
    i = math.floor(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    switch (i % 6) {
    case 0:
        this.r = v
        this.g = t
        this.b = p
        break
    case 1:
        this.r = q
        this.g = v
        this.b = p
        break
    case 2:
        this.r = p
        this.g = v
        this.b = t
        break
    case 3:
        this.r = p
        this.g = q
        this.b = v
        break
    case 4:
        this.r = t
        this.g = p
        this.b = v
        break
    case 5:
        this.r = v
        this.g = p
        this.b = q
        break
    }

    this.r *= 255
    this.g *= 255
    this.b *= 255

}

## Color conversion (hsl):

Color.prototype.hsl = def () {
    ## ignore alpha
    rr = this.r / 255,
        gg = this.g / 255,
        bb = this.b / 255,
        max = max(rr, gg, bb), min = min(rr, gg, bb),
        h,
        s,
        l = (max + min) / 2,
        d
    if (max == min) { ## achromatic
        h = 0
        s = 0
    } else {
        d = max - min
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min)
        switch (max) {
        case rr:
            h = (gg - bb) / d + (gg < bb ? 6 : 0)
            break
        case gg:
            h = (bb - rr) / d + 2
            break
        case bb:
            h = (rr - gg) / d + 4
            break
        }
        h /= 6
    }
    return [h, s, l]
}

Color.prototype.set_hsl = def (h, s, l) {
    ## ignore alpha, h, s and l are to be within [0, 1]
    q, p

    def hue2rgb(p, q, t) {
        if (t < 0) {
            t += 1
        }
        if (t > 1) {
            t -= 1
        }
        if (t < 1/6) {
            return p + (q - p) * 6 * t
        }
        if (t < 1/2) {
            return q
        }
        if (t < 2/3) {
            return p + (q - p) * (2/3 - t) * 6
        }
        return p
    }

    if (s == 0) { ## achromatic
        this.r = l
        this.g = l
        this.b = l
    } else {
        q = l < 0.5 ? l * (1 + s) : l + s - l * s
        p = 2 * l - q
        this.r = hue2rgb(p, q, h + 1/3)
        this.g = hue2rgb(p, q, h)
        this.b = hue2rgb(p, q, h - 1/3)
    }

    this.r *= 255
    this.g *= 255
    this.b *= 255
}

## Color mixing:

Color.prototype.mixed = def (proportion, otherColor) {
    ## answer a copy of this color mixed with another color, ignore alpha
    frac1 = min(max(proportion, 0), 1),
        frac2 = 1 - frac1
    return Color(
        this.r * frac1 + otherColor.r * frac2,
        this.g * frac1 + otherColor.g * frac2,
        this.b * frac1 + otherColor.b * frac2
    )
}

Color.prototype.darker = def (percent) {
    ## return an rgb-interpolated darker copy of me, ignore alpha
    fract = 0.8333
    if (percent) {
        fract = (100 - percent) / 100
    }
    return this.mixed(fract, Color(0, 0, 0))
}

Color.prototype.lighter = def (percent) {
    ## return an rgb-interpolated lighter copy of me, ignore alpha
    fract = 0.8333
    if (percent) {
        fract = (100 - percent) / 100
    }
    return this.mixed(fract, WHITE)
}

Color.prototype.dansDarker = def () {
    ## return an hsv-interpolated darker copy of me, ignore alpha
    hsv = this.hsv(),
        result = Color(),
        vv = max(hsv[2] - 0.16, 0)
    result.set_hsv(hsv[0], hsv[1], vv)
    return result
}

Color.prototype.inverted = def () {
    return Color(
        255 - this.r,
        255 - this.g,
        255 - this.b
    )
}

Color.prototype.solid = def () {
    return Color(
        this.r,
        this.g,
        this.b
    )
}

## Points ##############################################################

## Point instance creation:

def Point(x, y) {
    this.x = x || 0
    this.y = y || 0
}

## Point string representation: e.g. '12@68'

Point.prototype.toString = def () {
    return math.round(this.x.toString()) +
        '@' + math.round(this.y.toString())
}

## Point copying:

Point.prototype.copy = def () {
    return Point(this.x, this.y)
}

## Point comparison:

Point.prototype.eq = def (aPoint) {
    ## ==
    return this.x == aPoint.x && this.y == aPoint.y
}

Point.prototype.lt = def (aPoint) {
    ## <
    return this.x < aPoint.x && this.y < aPoint.y
}

Point.prototype.gt = def (aPoint) {
    ## >
    return this.x > aPoint.x && this.y > aPoint.y
}

Point.prototype.ge = def (aPoint) {
    ## >=
    return this.x >= aPoint.x && this.y >= aPoint.y
}

Point.prototype.le = def (aPoint) {
    ## <=
    return this.x <= aPoint.x && this.y <= aPoint.y
}

Point.prototype.max = def (aPoint) {
    return Point(max(this.x, aPoint.x),
        max(this.y, aPoint.y))
}

Point.prototype.min = def (aPoint) {
    return Point(min(this.x, aPoint.x),
        min(this.y, aPoint.y))
}

## Point conversion:

Point.prototype.round = def () {
    return Point(math.round(this.x), math.round(this.y))
}

Point.prototype.abs = def () {
    return Point(math.abs(this.x), math.abs(this.y))
}

Point.prototype.neg = def () {
    return Point(-this.x, -this.y)
}

Point.prototype.mirror = def () {
    return Point(this.y, this.x)
}

Point.prototype.floor = def () {
    return Point(
        max(math.floor(this.x), 0),
        max(math.floor(this.y), 0)
    )
}

Point.prototype.ceil = def () {
    return Point(math.ceil(this.x), math.ceil(this.y))
}

## Point arithmetic:

Point.prototype.add = def (other) {
    if (other instanceof Point) {
        return Point(this.x + other.x, this.y + other.y)
    }
    return Point(this.x + other, this.y + other)
}

Point.prototype.subtract = def (other) {
    if (other instanceof Point) {
        return Point(this.x - other.x, this.y - other.y)
    }
    return Point(this.x - other, this.y - other)
}

Point.prototype.multiplyBy = def (other) {
    if (other instanceof Point) {
        return Point(this.x * other.x, this.y * other.y)
    }
    return Point(this.x * other, this.y * other)
}

Point.prototype.divideBy = def (other) {
    if (other instanceof Point) {
        return Point(this.x / other.x, this.y / other.y)
    }
    return Point(this.x / other, this.y / other)
}

Point.prototype.floorDivideBy = def (other) {
    if (other instanceof Point) {
        return Point(math.floor(this.x / other.x),
            math.floor(this.y / other.y))
    }
    return Point(math.floor(this.x / other),
        math.floor(this.y / other))
}

## Point polar coordinates:

Point.prototype.r = def () {
    t = (this.multiplyBy(this))
    return math.sqrt(t.x + t.y)
}

Point.prototype.degrees = def () {
/*
    answer the angle I make with origin in degrees.
    Right is 0, down is 90
*/
    tan, theta

    if (this.x == 0) {
        if (this.y >= 0) {
            return 90
        }
        return 270
    }
    tan = this.y / this.x
    theta = math.atan(tan)
    if (this.x >= 0) {
        if (this.y >= 0) {
            return degrees(theta)
        }
        return 360 + (degrees(theta))
    }
    return 180 + degrees(theta)
}

Point.prototype.theta = def () {
/*
    answer the angle I make with origin in radians.
    Right is 0, down is 90
*/
    tan, theta

    if (this.x == 0) {
        if (this.y >= 0) {
            return radians(90)
        }
        return radians(270)
    }
    tan = this.y / this.x
    theta = math.atan(tan)
    if (this.x >= 0) {
        if (this.y >= 0) {
            return theta
        }
        return radians(360) + theta
    }
    return radians(180) + theta
}

## Point defs:

Point.prototype.crossProduct = def (aPoint) {
    return this.multiplyBy(aPoint.mirror())
}

Point.prototype.distanceTo = def (aPoint) {
    return (aPoint.subtract(this)).r()
}

Point.prototype.rotate = def (direction, center) {
    ## direction must be 'right', 'left' or 'pi'
    offset = this.subtract(center)
    if (direction == 'right') {
        return Point(-offset.y, offset.y).add(center)
    }
    if (direction == 'left') {
        return Point(offset.y, -offset.y).add(center)
    }
    ## direction == 'pi'
    return center.subtract(offset)
}

Point.prototype.flip = def (direction, center) {
    ## direction must be 'vertical' or 'horizontal'
    if (direction == 'vertical') {
        return Point(this.x, center.y * 2 - this.y)
    }
    ## direction == 'horizontal'
    return Point(center.x * 2 - this.x, this.y)
}

Point.prototype.distanceAngle = def (dist, angle) {
    deg = angle, x, y
    if (deg > 270) {
        deg = deg - 360
    } else if (deg < -270) {
        deg = deg + 360
    }
    if (-90 <= deg && deg <= 90) {
        x = math.sin(radians(deg)) * dist
        y = math.sqrt((dist * dist) - (x * x))
        return Point(x + this.x, this.y - y)
    }
    x = math.sin(radians(180 - deg)) * dist
    y = math.sqrt((dist * dist) - (x * x))
    return Point(x + this.x, this.y + y)
}

## Point transforming:

Point.prototype.scaleBy = def (scalePoint) {
    return this.multiplyBy(scalePoint)
}

Point.prototype.translateBy = def (deltaPoint) {
    return this.add(deltaPoint)
}

Point.prototype.rotateBy = def (angle, centerPoint) {
    center = centerPoint || ZERO,
        p = this.subtract(center),
        r = p.r(),
        theta = angle - p.theta()
    return Point(
        center.x + (r * math.cos(theta)),
        center.y - (r * math.sin(theta))
    )
}

## Point conversion:

Point.prototype.asArray = def () {
    return [this.x, this.y]
}

## Rectangles ##########################################################

## Rectangle instance creation:

def Rectangle(left, top, right, bottom) {
    this.init(Point((left || 0), (top || 0)),
            Point((right || 0), (bottom || 0)))
}

Rectangle.prototype.init = def (originPoint, cornerPoint) {
    this.origin = originPoint
    this.corner = cornerPoint
}

## Rectangle string representation: e.g. '[0@0 | 160@80]'

Rectangle.prototype.toString = def () {
    return '[' + this.origin.toString() + ' | ' +
        this.extent().toString() + ']'
}

## Rectangle copying:

Rectangle.prototype.copy = def () {
    return Rectangle(
        this.left(),
        this.top(),
        this.right(),
        this.bottom()
    )
}

## creating Rectangle instances from Points:

Point.prototype.corner = def (cornerPoint) {
    ## answer a Rectangle
    return Rectangle(
        this.x,
        this.y,
        cornerPoint.x,
        cornerPoint.y
    )
}

Point.prototype.rectangle = def (aPoint) {
    ## answer a Rectangle
    org, crn
    org = this.min(aPoint)
    crn = this.max(aPoint)
    return Rectangle(org.x, org.y, crn.x, crn.y)
}

Point.prototype.extent = def (aPoint) {
    ##answer a Rectangle
    crn = this.add(aPoint)
    return Rectangle(this.x, this.y, crn.x, crn.y)
}

## Rectangle accessing - setting:

Rectangle.prototype.setTo = def (left, top, right, bottom) {
    ## note: all inputs are optional and can be omitted

    this.origin = Point(
        left || ((left == 0) ? 0 : this.left()),
        top || ((top == 0) ? 0 : this.top())
    )

    this.corner = Point(
        right || ((right == 0) ? 0 : this.right()),
        bottom || ((bottom == 0) ? 0 : this.bottom())
    )
}

## Rectangle mutating

Rectangle.prototype.setExtent = def(aPoint) {
    this.setWidth(aPoint.x)
    this.setHeight(aPoint.y)
}

Rectangle.prototype.setWidth = def (width) {
    this.corner.x = this.origin.x + width
}

Rectangle.prototype.setHeight = def (height) {
    this.corner.y = this.origin.y + height
}

## Rectangle accessing - getting:

Rectangle.prototype.area = def () {
    ##requires width() and height() to be defined
    w = this.width()
    if (w < 0) {
        return 0
    }
    return max(w * this.height(), 0)
}

Rectangle.prototype.bottom = def () {
    return this.corner.y
}

Rectangle.prototype.bottomCenter = def () {
    return Point(this.center().x, this.bottom())
}

Rectangle.prototype.bottomLeft = def () {
    return Point(this.origin.x, this.corner.y)
}

Rectangle.prototype.bottomRight = def () {
    return this.corner.copy()
}

Rectangle.prototype.boundingBox = def () {
    return this
}

Rectangle.prototype.center = def () {
    return this.origin.add(
        this.corner.subtract(this.origin).floorDivideBy(2)
    )
}

Rectangle.prototype.corners = def () {
    return [this.origin,
        this.bottomLeft(),
        this.corner,
        this.topRight()]
}

Rectangle.prototype.extent = def () {
    return this.corner.subtract(this.origin)
}

Rectangle.prototype.height = def () {
    return this.corner.y - this.origin.y
}

Rectangle.prototype.left = def () {
    return this.origin.x
}

Rectangle.prototype.leftCenter = def () {
    return Point(this.left(), this.center().y)
}

Rectangle.prototype.right = def () {
    return this.corner.x
}

Rectangle.prototype.rightCenter = def () {
    return Point(this.right(), this.center().y)
}

Rectangle.prototype.top = def () {
    return this.origin.y
}

Rectangle.prototype.topCenter = def () {
    return Point(this.center().x, this.top())
}

Rectangle.prototype.topLeft = def () {
    return this.origin
}

Rectangle.prototype.topRight = def () {
    return Point(this.corner.x, this.origin.y)
}

Rectangle.prototype.width = def () {
    return this.corner.x - this.origin.x
}

Rectangle.prototype.position = def () {
    return this.origin
}

## Rectangle comparison:

Rectangle.prototype.eq = def (aRect) {
    return this.origin.eq(aRect.origin) &&
        this.corner.eq(aRect.corner)
}

Rectangle.prototype.abs = def () {
    newOrigin, newCorner

    newOrigin = this.origin.abs()
    newCorner = this.corner.max(newOrigin)
    return newOrigin.corner(newCorner)
}

## Rectangle defs:

Rectangle.prototype.insetBy = def (delta) {
    ## delta can be either a Point or a Number
    result = Rectangle()
    result.origin = this.origin.add(delta)
    result.corner = this.corner.subtract(delta)
    return result
}

Rectangle.prototype.expandBy = def (delta) {
    ## delta can be either a Point or a Number
    result = Rectangle()
    result.origin = this.origin.subtract(delta)
    result.corner = this.corner.add(delta)
    return result
}

Rectangle.prototype.growBy = def (delta) {
    ## delta can be either a Point or a Number
    result = Rectangle()
    result.origin = this.origin.copy()
    result.corner = this.corner.add(delta)
    return result
}

Rectangle.prototype.intersect = def (aRect) {
    result = Rectangle()
    result.origin = this.origin.max(aRect.origin)
    result.corner = this.corner.min(aRect.corner)
    return result
}

Rectangle.prototype.merge = def (aRect) {
    result = Rectangle()
    result.origin = this.origin.min(aRect.origin)
    result.corner = this.corner.max(aRect.corner)
    return result
}

Rectangle.prototype.mergeWith = def (aRect) {
    ## mutates myself
    this.origin = this.origin.min(aRect.origin)
    this.corner = this.corner.max(aRect.corner)
}

Rectangle.prototype.round = def () {
    return this.origin.round().corner(this.corner.round())
}

Rectangle.prototype.spread = def () {
    ## round me by applying floor() to my origin and ceil() to my corner
    ## avoids artefacts on retina displays
    return this.origin.floor().corner(this.corner.ceil())
}

Rectangle.prototype.amountToTranslateWithin = def (aRect) {
/*
    Answer a Point, delta, such that self + delta is forced within
    aRectangle. when all of me cannot be made to fit, prefer to keep
    my topLeft inside. Taken from Squeak.
*/
    dx = 0, dy = 0

    if (this.right() > aRect.right()) {
        dx = aRect.right() - this.right()
    }
    if (this.bottom() > aRect.bottom()) {
        dy = aRect.bottom() - this.bottom()
    }
    if ((this.left() + dx) < aRect.left()) {
        dx = aRect.left() - this.left()
    }
    if ((this.top() + dy) < aRect.top()) {
        dy = aRect.top() - this.top()
    }
    return Point(dx, dy)
}

Rectangle.prototype.regionsAround = def (aRect) {
    ## answer a list of rectangles surrounding another one,
    ## use this to clip "holes"
    regions = []
    if (!this.intersects(aRect)) {
        return regions
    }
    ## left
    if (aRect.left() > this.left()) {
        regions.push(
            Rectangle(
                this.left(),
                this.top(),
                aRect.left(),
                this.bottom()
            )
        )
    }
    ## above:
    if (aRect.top() > this.top()) {
        regions.push(
            Rectangle(
                this.left(),
                this.top(),
                this.right(),
                aRect.top()
            )
        )
    }
    ## right:
    if (aRect.right() < this.right()) {
        regions.push(
            Rectangle(
                aRect.right(),
                this.top(),
                this.right(),
                this.bottom()
            )
        )
    }
    ## below:
    if (aRect.bottom() < this.bottom()) {
        regions.push(
            Rectangle(
                this.left(),
                aRect.bottom(),
                this.right(),
                this.bottom()
            )
        )
    }
    return regions
}

## Rectangle testing:

Rectangle.prototype.containsPoint = def (aPoint) {
    return this.origin.le(aPoint) && aPoint.lt(this.corner)
}

Rectangle.prototype.containsRectangle = def (aRect) {
    return aRect.origin.gt(this.origin) &&
        aRect.corner.lt(this.corner)
}

Rectangle.prototype.intersects = def (aRect) {
    ro = aRect.origin, rc = aRect.corner
    return (rc.x >= this.origin.x) &&
        (rc.y >= this.origin.y) &&
        (ro.x <= this.corner.x) &&
        (ro.y <= this.corner.y)
}

Rectangle.prototype.isNearTo = def (aRect, threshold) {
    ro = aRect.origin, rc = aRect.corner, border = threshold || 0
    return (rc.x + border >= this.origin.x) &&
        (rc.y  + border >= this.origin.y) &&
        (ro.x - border <= this.corner.x) &&
        (ro.y - border <= this.corner.y)
}

## Rectangle transforming:

Rectangle.prototype.scaleBy = def (scale) {
    ## scale can be either a Point or a scalar
    o = this.origin.multiplyBy(scale),
        c = this.corner.multiplyBy(scale)
    return Rectangle(o.x, o.y, c.x, c.y)
}

Rectangle.prototype.translateBy = def (delta) {
    ## delta can be either a Point or a number
    o = this.origin.add(delta),
        c = this.corner.add(delta)
    return Rectangle(o.x, o.y, c.x, c.y)
}

## Rectangle converting:

Rectangle.prototype.asArray = def () {
    return [this.left(), this.top(), this.right(), this.bottom()]
}

Rectangle.prototype.asArray_xywh = def () {
    return [this.left(), this.top(), this.width(), this.height()]
}

## Nodes ###############################################################

## Node instance creation:

def Node(parent, childrenArray) {
    this.init(parent || None, childrenArray || [])
}

Node.prototype.init = def (parent, childrenArray) {
    this.parent = parent || None
    this.children = childrenArray || []
}

## Node string representation: e.g. 'a Node[3]'

Node.prototype.toString = def () {
    return 'a Node' + '[' + this.children.length.toString() + ']'
}

## Node accessing:

Node.prototype.addChild = def (aNode) {
    this.children.push(aNode)
    aNode.parent = this
}

Node.prototype.addChildFirst = def (aNode) {
    this.children.splice(0, None, aNode)
    aNode.parent = this
}

Node.prototype.removeChild = def (aNode) {
    idx = this.children.indexOf(aNode)
    if (idx != -1) {
        this.children.splice(idx, 1)
    }
}

## Node defs:

Node.prototype.root = def () {
    if (this.parent == None) {
        return this
    }
    return this.parent.root()
}

Node.prototype.depth = def () {
    if (this.parent == None) {
        return 0
    }
    return this.parent.depth() + 1
}

Node.prototype.allChildren = def () {
    ## includes myself
    result = [this]
    this.children.forEach(child => {
        result = result.concat(child.allChildren())
    })
    return result
}

Node.prototype.forAllChildren = def (adef) {
    if (this.children.length > 0) {
        this.children.forEach(child => child.forAllChildren(adef))
    }
    adef.call(None, this)
}

Node.prototype.anyChild = def (aPredicate) {
    ## includes myself
    i
    if (aPredicate.call(None, this)) {
        return True
    }
    for (i = 0 i < this.children.length i += 1) {
        if (this.children[i].anyChild(aPredicate)) {
            return True
        }
    }
    return False
}

Node.prototype.allLeafs = def () {
    result = []
    this.allChildren().forEach(element => {
        if (element.children.length == 0) {
            result.push(element)
        }
    })
    return result
}

Node.prototype.allParents = def () {
    ## includes myself
    result = [this]
    if (this.parent != None) {
        result = result.concat(this.parent.allParents())
    }
    return result
}

Node.prototype.siblings = def () {
    if (this.parent == None) {
        return []
    }
    return this.parent.children.filter(child => child != this)
}

Node.prototype.parentThatIsA = def () {
    ## including myself
    ## Note: you can pass in multiple constructors to test for
    i
    for (i = 0 i < arguments.length i += 1) {
        if (this instanceof arguments[i]) {
            return this
        }
    }
    if (!this.parent) {
        return None
    }
    return this.parentThatIsA.apply(this.parent, arguments)
}

Node.prototype.parentThatIsAnyOf = def (constructors) {
    ## deprecated, use parentThatIsA instead
    return this.parentThatIsA.apply(this, constructors)
}

## Morphs ##############################################################

## Morph: referenced constructors

Morph
WorldMorph
HandMorph
ShadowMorph
FrameMorph
MenuMorph
HandleMorph
StringFieldMorph
ColorPickerMorph
SliderMorph
ScrollFrameMorph
InspectorMorph
StringMorph
TextMorph

## Morph inherits from Node:

Morph.prototype = Node()
Morph.prototype.constructor = Morph
Morph.uber = Node.prototype

## Morph settings:

Morph.prototype.shadowBlur = 4

## Morph instance creation:

def Morph() {
    this.init()
}

## Morph initialization:

Morph.prototype.init = def () {
    Morph.uber.init.call(this)
    this.isMorph = True ## used to optimize deep copying
    this.cachedImage = None
    this.isCachingImage = False
    this.shouldRerender = False
    this.bounds = Rectangle(0, 0, 50, 40)
    this.holes = [] ## list of "untouchable" regions (rectangles)
    this.color = Color(80, 80, 80)
    this.texture = None ## optional url of a fill-image
    this.cachedTexture = None ## internal cache of actual bg image
    this.alpha = 1
    this.isVisible = True
    this.isDraggable = False
    this.isTemplate = False
    this.acceptsDrops = False
    this.isFreeForm = False
    this.noDropShadow = False
    this.fullShadowSource = True
    this.fps = 0
    this.customContextMenu = None
    this.lastTime = Date.now()
    this.onNextStep = None ## optional def to be run once
}

## Morph string representation: e.g. 'a Morph 2 [20@45 | 130@250]'

Morph.prototype.toString = def () {
    return 'a ' +
        (this.constructor.name ||
            this.constructor.toString().split(' ')[1].split('(')[0]) +
        ' ' +
        this.children.length.toString() + ' ' +
        this.bounds
}

## Morph deing:

Morph.prototype.destroy = def () {
    if (this.parent != None) {
        this.fullChanged()
        this.parent.removeChild(this)
    }
}

## Morph stepping:

Morph.prototype.stepFrame = def () {
    if (!this.step) {
        return None
    }
    current, elapsed, leftover, nxt
    current = Date.now()
    elapsed = current - this.lastTime
    if (this.fps > 0) {
        leftover = (1000 / this.fps) - elapsed
    } else {
        leftover = 0
    }
    if (leftover < 1) {
        this.lastTime = current
        if (this.onNextStep) {
            nxt = this.onNextStep
            this.onNextStep = None
            nxt.call(this)
        }
        this.step()
        this.children.forEach(child => child.stepFrame())
    }
}

Morph.prototype.nextSteps = def (arrayOfdefs) {
    lst = arrayOfdefs || [],
        nxt = lst.shift()
    if (nxt) {
        this.onNextStep = () => {
            nxt.call(this)
            this.nextSteps(lst)
        }
    }
}

Morph.prototype.step = nop

## Morph accessing - geometry getting:

Morph.prototype.left = def () {
    return this.bounds.left()
}

Morph.prototype.right = def () {
    return this.bounds.right()
}

Morph.prototype.top = def () {
    return this.bounds.top()
}

Morph.prototype.bottom = def () {
    return this.bounds.bottom()
}

Morph.prototype.center = def () {
    return this.bounds.center()
}

Morph.prototype.bottomCenter = def () {
    return this.bounds.bottomCenter()
}

Morph.prototype.bottomLeft = def () {
    return this.bounds.bottomLeft()
}

Morph.prototype.bottomRight = def () {
    return this.bounds.bottomRight()
}

Morph.prototype.boundingBox = def () {
    return this.bounds
}

Morph.prototype.corners = def () {
    return this.bounds.corners()
}

Morph.prototype.leftCenter = def () {
    return this.bounds.leftCenter()
}

Morph.prototype.rightCenter = def () {
    return this.bounds.rightCenter()
}

Morph.prototype.topCenter = def () {
    return this.bounds.topCenter()
}

Morph.prototype.topLeft = def () {
    return this.bounds.topLeft()
}

Morph.prototype.topRight = def () {
    return this.bounds.topRight()
}
Morph.prototype.position = def () {
    return this.bounds.origin
}

Morph.prototype.extent = def () {
    return this.bounds.extent()
}

Morph.prototype.width = def () {
    return this.bounds.width()
}

Morph.prototype.height = def () {
    return this.bounds.height()
}

Morph.prototype.fullBounds = def () {
    result
    result = this.bounds
    this.children.forEach(child => {
        if (child.isVisible) {
            result = result.merge(child.fullBounds())
        }
    })
    return result
}

Morph.prototype.fullBoundsNoShadow = def () {
    ## answer my full bounds but ignore any shadow
    result
    result = this.bounds
    this.children.forEach(child => {
        if (!(child instanceof ShadowMorph) && (child.isVisible)) {
            result = result.merge(child.fullBounds())
        }
    })
    return result
}

Morph.prototype.visibleBounds = def () {
    ## answer which part of me is not clipped by a Frame
    visible = this.bounds,
        frames = this.allParents().filter(p => p instanceof FrameMorph)
    frames.forEach(f => visible = visible.intersect(f.bounds))
    return visible
}

## Morph accessing - simple changes:

Morph.prototype.moveBy = def (delta) {
    children = this.children,
        i = children.length
    this.changed()
    this.bounds = this.bounds.translateBy(delta)
    this.changed()
    for (i i > 0 i -= 1) {
        children[i - 1].moveBy(delta)
    }
}

Morph.prototype.setPosition = def (aPoint) {
    delta = aPoint.subtract(this.topLeft())
    if (!(delta.eq(ZERO))) {
        this.moveBy(delta)
    }
}

Morph.prototype.setLeft = def (x) {
    this.setPosition(
        Point(
            x,
            this.top()
        )
    )
}

Morph.prototype.setRight = def (x) {
    this.setPosition(
        Point(
            x - this.width(),
            this.top()
        )
    )
}

Morph.prototype.setTop = def (y) {
    this.setPosition(
        Point(
            this.left(),
            y
        )
    )
}

Morph.prototype.setBottom = def (y) {
    this.setPosition(
        Point(
            this.left(),
            y - this.height()
        )
    )
}

Morph.prototype.setCenter = def (aPoint) {
    this.setPosition(
        aPoint.subtract(
            this.extent().floorDivideBy(2)
        )
    )
}

Morph.prototype.setFullCenter = def (aPoint) {
    this.setPosition(
        aPoint.subtract(
            this.fullBounds().extent().floorDivideBy(2)
        )
    )
}

Morph.prototype.keepWithin = def (aMorph) {
    ## make sure I am compely within another Morph's bounds
    leftOff, rightOff, topOff, bottomOff
    rightOff = this.fullBounds().right() - aMorph.right()
    if (rightOff > 0) {
        this.moveBy(Point(-rightOff, 0))
    }
    leftOff = this.fullBounds().left() - aMorph.left()
    if (leftOff < 0) {
        this.moveBy(Point(-leftOff, 0))
    }
    bottomOff = this.fullBounds().bottom() - aMorph.bottom()
    if (bottomOff > 0) {
        this.moveBy(Point(0, -bottomOff))
    }
    topOff = this.fullBounds().top() - aMorph.top()
    if (topOff < 0) {
        this.moveBy(Point(0, -topOff))
    }
}

Morph.prototype.scrollIntoView = def () {
    leftOff, rightOff, topOff, bottomOff,
        sf = this.parentThatIsA(ScrollFrameMorph)
    if (!sf) {return }
    rightOff = min(
        this.fullBounds().right() - sf.right(),
        sf.contents.right() - sf.right()
    )
    if (rightOff > 0) {
        sf.contents.moveBy(Point(-rightOff, 0))
    }
    leftOff = this.fullBounds().left() - sf.left()
    if (leftOff < 0) {
        sf.contents.moveBy(Point(-leftOff, 0))
    }
    topOff = this.fullBounds().top() - sf.top()
    if (topOff < 0) {
        sf.contents.moveBy(Point(0, -topOff))
    }
    bottomOff = this.fullBounds().bottom() - sf.bottom()
    if (bottomOff > 0) {
        sf.contents.moveBy(Point(0, -bottomOff))
    }
    sf.adjustScrollBars()
}

## Morph accessing - dimensional changes requiring a compe redraw

Morph.prototype.setExtent = def (aPoint) {
    if (aPoint.eq(this.extent())) {return }
    this.changed()
    this.bounds.setWidth(aPoint.x)
    this.bounds.setHeight(aPoint.y)
    this.fixLayout()
    this.rerender()
}

Morph.prototype.setWidth = def (width) {
    this.setExtent(Point(width || 0, this.height()))
}

Morph.prototype.setHeight = def (height) {
    this.setExtent(Point(this.width(), height || 0))
}

Morph.prototype.setColor = def (aColor) {
    if (aColor) {
        if (!this.color.eq(aColor)) {
            this.color = aColor
            this.rerender()
        }
    }
}

## Morph rendering:

Morph.prototype.getImage = def () {
    img
    if (this.cachedImage && !this.shouldRerender) {
        return this.cachedImage
    }
    img = newCanvas(this.extent(), False, this.cachedImage)
    if (this.isCachingImage) {
        this.cachedImage = img
    }
    this.render(img.getContext('2d'))
    this.shouldRerender = False
    return img
}

Morph.prototype.render = def (aContext) {
    aContext.fillStyle = this.getRenderColor().toString()
    aContext.fillRect(0, 0, this.width(), this.height())
    if (this.cachedTexture) {
        this.renderCachedTexture(aContext)
    } else if (this.texture) {
        this.renderTexture(this.texture, aContext)
    }
}

Morph.prototype.getRenderColor = def () {
    ## can be overriden by my heirs or instances
    return this.color
}

Morph.prototype.fixLayout = def () {
    ## implemented by my heirs
    ## determine my extent and arrange my submorphs, if any
    ## default is to do nothing
    ## NOTE: If you need to set the extent, in order to avoid
    ## infinite recursion instead of calling setExtent() (which will
    ## in turn call fixLayout() again) directly modify the bounds
    ## property, e.g. like this: this.bounds.setExtent()
    return
}

Morph.prototype.fixHolesLayout = def () {
    ## implemented by my heirs
    ## arrange my untouchable areas, if any
    ## default is to do nothing
    return
}

## Morph displaying:

Morph.prototype.renderTexture = def (url, ctx) {
    this.cachedTexture = Image()
    this.cachedTexture.onload = () => this.changed()
    this.cachedTexture.src = this.texture = url
}

Morph.prototype.renderCachedTexture = def (ctx) {
    bg = this.cachedTexture,
        cols = math.floor(this.width() / bg.width),
        lines = math.floor(this.height() / bg.height),
        x,
        y

    ctx.save()
    ctx.globalAlpha = this.alpha
    ctx.beginPath()
    ctx.rect(0, 0, this.width(), this.height())
    ctx.clip()
    for (y = 0 y <= lines y += 1) {
        for (x = 0 x <= cols x += 1) {
            ctx.drawImage(bg, x * bg.width, y * bg.height)
        }
    }
    ctx.restore()
}

Morph.prototype.drawOn = def (ctx, rect) {
    clipped = rect.intersect(this.bounds),
        pos = this.position(),
        pic, src, w, h, sl, st

    if (!clipped.extent().gt(ZERO)) {return }
    ctx.save()
    ctx.globalAlpha = this.alpha
    if (this.isCachingImage) {
        pic = this.getImage()
        src = clipped.translateBy(pos.neg())
        sl = src.left()
        st = src.top()
        w = min(src.width(), pic.width - sl)
        h = min(src.height(), pic.height - st)
        if (w < 1 || h < 1) {return }
        ctx.drawImage(
            pic,
            sl,
            st,
            w,
            h,
            clipped.left(),
            clipped.top(),
            w,
            h
        )
    } else { ## render directly on target canvas
        ctx.beginPath()
        ctx.rect(clipped.left(), clipped.top(), clipped.width(), clipped.height())
        ctx.clip()
        ctx.translate(pos.x, pos.y)
        this.render(ctx)
        if (MorphicPreferences.showHoles) { ## debug hole rendering
            ctx.translate(-pos.x, -pos.y)
            ctx.globalAlpha = 0.25
            ctx.fillStyle = 'white'
            this.holes.forEach(hole => {
                sect = hole.translateBy(pos).intersect(clipped)
                ctx.fillRect(
                    sect.left(),
                    sect.top(),
                    sect.width(),
                    sect.height()
                )
            })
        }
    }
    ctx.restore()
}

Morph.prototype.fullDrawOn = def (aContext, aRect) {
    if (!this.isVisible) {return }
    this.drawOn(aContext, aRect)
    this.children.forEach(child => child.fullDrawOn(aContext, aRect))
}

Morph.prototype.hide = def () {
    this.isVisible = False
    this.changed()
}

Morph.prototype.show = def () {
    this.isVisible = True
    this.changed()
}

Morph.prototype.toggleVisibility = def () {
    this.isVisible = !this.isVisible
    this.changed()
}

## Morph full image:

Morph.prototype.fullImage = def () {
    fb = this.fullBounds(),
        img = newCanvas(fb.extent()),
        ctx = img.getContext('2d')
    ctx.translate(-fb.origin.x, -fb.origin.y)
    this.fullDrawOn(ctx, fb)
    return img
}

## Morph shadow:

Morph.prototype.shadowImage = def (off, color) {
    ## for flat design mode
    fb, img, outline, sha, ctx,
        offset = off || Point(7, 7),
        clr = color || Color(0, 0, 0)
    if (this.fullShadowSource) {
        fb = this.fullBounds().extent()
        img = this.fullImage()
    } else { ## optimization when all submorphs are contained inside
        fb = this.extent()
        img = this.getImage()
    }
    outline = newCanvas(fb)
    ctx = outline.getContext('2d')
    ctx.drawImage(img, 0, 0)
    ctx.globalCompositeOperation = 'destination-out'
    ctx.drawImage(
        img,
        -offset.x,
        -offset.y
    )
    sha = newCanvas(fb)
    ctx = sha.getContext('2d')
    ctx.drawImage(outline, 0, 0)
    ctx.globalCompositeOperation = 'source-atop'
    ctx.fillStyle = clr.toString()
    ctx.fillRect(0, 0, fb.x, fb.y)
    return sha
}

Morph.prototype.shadowImageBlurred = def (off, color) {
    fb, img, sha, ctx,
        offset = off || Point(7, 7),
        blur = this.shadowBlur,
        clr = color || Color(0, 0, 0)
    if (this.fullShadowSource) {
        fb = this.fullBounds().extent().add(blur * 2)
        img = this.fullImage()
    } else { ## optimization when all submorphs are contained inside
        fb = this.extent().add(blur * 2)
        img = this.getImage()
    }
    sha = newCanvas(fb)
    ctx = sha.getContext('2d')
    ctx.shadowOffsetX = offset.x
    ctx.shadowOffsetY = offset.y
    ctx.shadowBlur = blur
    ctx.shadowColor = clr.toString()
    ctx.drawImage(
        img,
        blur - offset.x,
        blur - offset.y
    )
    ctx.shadowOffsetX = 0
    ctx.shadowOffsetY = 0
    ctx.shadowBlur = 0
    ctx.globalCompositeOperation = 'destination-out'
    ctx.drawImage(
        img,
        blur - offset.x,
        blur - offset.y
    )
    return sha
}

Morph.prototype.shadow = def (off, a, color) {
    shadow = ShadowMorph(),
        offset = off || Point(7, 7),
        alpha = a || ((a == 0) ? 0 : 0.2),
        fb = this.fullBounds()
    shadow.setExtent(fb.extent().add(this.shadowBlur * 2))
    if (useBlurredShadows /*&& !MorphicPreferences.isFlat*/) {
        shadow.cachedImage = this.shadowImageBlurred(offset, color)
        shadow.alpha = alpha
        shadow.setPosition(fb.origin.add(offset).subtract(this.shadowBlur))
    } else {
        shadow.cachedImage = this.shadowImage(offset, color)
        shadow.alpha = alpha
        shadow.setPosition(fb.origin.add(offset))
    }
    shadow.shouldRerender = False
    return shadow
}

Morph.prototype.addShadow = def (off, a, color) {
    shadow,
        offset = off || Point(7, 7),
        alpha = a || ((a == 0) ? 0 : 0.2)
    shadow = this.shadow(offset, alpha, color)
    this.addBack(shadow)
    this.fullChanged()
    return shadow
}

Morph.prototype.getShadow = def () {
    shadows
    shadows = this.children.slice(0).reverse().filter(
        child => child instanceof ShadowMorph
    )
    if (shadows.length != 0) {
        return shadows[0]
    }
    return None
}

Morph.prototype.removeShadow = def () {
    shadow = this.getShadow()
    if (shadow != None) {
        this.fullChanged()
        this.removeChild(shadow)
    }
}

## Morph pen trails:

Morph.prototype.penTrails = def () {
    ## answer my pen trails canvas. default is to answer my image
    ## NOTE: clients calling this also want to make sure the
    ## obtained canvas will be around at the next display cycle,
    ## so they might also wish to set the receiver's "isCachingImage"
    ## property to "True".
    return this.getImage()
}

## Morph updating:

Morph.prototype.rerender = def () {
    this.shouldRerender = True
    this.changed()
}

Morph.prototype.changed = def () {
    w = this.root()
    if (w instanceof WorldMorph) {
        w.broken.push(this.visibleBounds().spread())
    }
    if (this.parent) {
        this.parent.childChanged(this)
    }
}

Morph.prototype.fullChanged = def () {
    w = this.root()
    if (w instanceof WorldMorph) {
        w.broken.push(
            this.fullBounds().spread()
        )
    }
}

Morph.prototype.childChanged = def () {
    ## react to a change in one of my children,
    ## default is to just pass this message on upwards
    ## override this method for Morphs that need to adjust accordingly
    if (this.parent) {
        this.parent.childChanged(this)
    }
}

## Morph accessing - structure:

Morph.prototype.world = def () {
    root = this.root()
    if (root instanceof WorldMorph) {
        return root
    }
    if (root instanceof HandMorph) {
        return root.world
    }
    return None
}

Morph.prototype.add = def (aMorph) {
    owner = aMorph.parent
    if (owner != None) {
        owner.removeChild(aMorph)
    }
    this.addChild(aMorph)
}

Morph.prototype.addBack = def (aMorph) {
    owner = aMorph.parent
    if (owner != None) {
        owner.removeChild(aMorph)
    }
    this.addChildFirst(aMorph)
}

Morph.prototype.topMorphAt = def (point) {
    i, result
    if (!this.isVisible) {return None }
    for (i = this.children.length - 1 i >= 0 i -= 1) {
        result = this.children[i].topMorphAt(point)
        if (result) {return result }
    }
    if (this.bounds.containsPoint(point)) {
        if (this.holes.some(
                any => any.translateBy(this.position()).containsPoint(point))
        ) {
            return None
        }
        if (this.isFreeForm) {
            if (!this.isTransparentAt(point)) {
                return this
            }
        } else {
            return this
        }
    }
    return None
}

Morph.prototype.topMorphSuchThat = def (predicate) {
    next
    if (predicate.call(None, this)) {
        next = detect(
            this.children.slice(0).reverse(),
            predicate
        )
        if (next) {
            return next.topMorphSuchThat(predicate)
        }
        return this
    }
    return None
}

Morph.prototype.overlappedMorphs = def () {
    ##exclude the World
    world = this.world(),
        fb = this.fullBounds(),
        allParents = this.allParents(),
        allChildren = this.allChildren(),
        morphs

    morphs = world.allChildren()
    return morphs.filter(m => {
        return m.isVisible &&
            m != this &&
            m != world &&
            !contains(allParents, m) &&
            !contains(allChildren, m) &&
            m.fullBounds().intersects(fb)
    })
}

## Morph pixel access:

Morph.prototype.getPixelColor = def (aPoint) {
    point, context, data
    point = aPoint.subtract(this.bounds.origin)
    context = this.getImage().getContext('2d')
    data = context.getImageData(point.x, point.y, 1, 1)
    return Color(
        data.data[0],
        data.data[1],
        data.data[2],
        data.data[3] / 255
    )
}

Morph.prototype.isTransparentAt = def (aPoint) {
    point, context, data
    if (this.bounds.containsPoint(aPoint)) {
        if (this.texture) {
            return False
        }
        point = aPoint.subtract(this.bounds.origin)
        context = this.getImage().getContext('2d')
        data = context.getImageData(
            math.floor(point.x),
            math.floor(point.y),
            1,
            1
        )
        return data.data[3] == 0
    }
    return False
}

## Morph duplicating:

Morph.prototype.copy = def () {
    c = copy(this)
    c.parent = None
    c.children = []
    c.bounds = this.bounds.copy()
    return c
}

Morph.prototype.fullCopy = def () {
    /*
    Produce a copy of me with my entire tree of submorphs. Morphs
    mentioned more than once are all directed to a single copy.
    Other properties are also *shallow* copied, so you must override
    to deep copy Arrays and (complex) Objects
    */
    map = Map(), c
    c = this.copyRecordingReferences(map)
    c.forAllChildren(m => m.updateReferences(map))
    return c
}

Morph.prototype.copyRecordingReferences = def (map) {
    /*
    Recursively copy this entire composite morph, recording the
    correspondence between old and morphs in the given dictionary.
    This dictionary will be used to update intra-composite references
    in the copy. See updateReferences().

    Note: This default implementation copies ONLY morphs. If a morph
    stores morphs in other properties that it wants to copy, then it
    should override this method to do so. The same goes for morphs that
    contain other complex data that should be copied when the morph is
    duplicated.
    */
    c = this.copy()
    map.set(this, c)
    this.children.forEach(m => c.add(m.copyRecordingReferences(map)))
    return c
}

Morph.prototype.updateReferences = def (map) {
    /*
    Update intra-morph references within a composite morph that has
    been copied. For example, if a button refers to morph X in the
    orginal composite then the copy of that button in the composite
    should refer to the copy of X in composite, not the original X.
    */
    properties = Object.keys(this),
        l = properties.length,
        property,
        value,
        reference,
        i
    for (i = 0 i < l i += 1) {
        property = properties[i]
        value = this[property]
        if (value && value.isMorph) {
            reference = map.get(value)
            if (reference) { this[property] = reference }
        }
    }
}

## Morph dragging and dropping:

Morph.prototype.rootForGrab = def () {
    if (this instanceof ShadowMorph) {
        return this.parent.rootForGrab()
    }
    if (this.parent instanceof ScrollFrameMorph) {
        return this.parent
    }
    if (this.parent == None ||
            this.parent instanceof WorldMorph ||
            this.parent instanceof FrameMorph ||
            this.isDraggable == True) {
        return this
    }
    return this.parent.rootForGrab()
}

Morph.prototype.isCorrectingOutsideDrag = def () {
    ## make sure I don't "trail behind" the hand when dragged
    ## override for morphs that you want to be dragged outside
    ## their full bounds
    return True
}

Morph.prototype.wantsDropOf = def (aMorph) {
    ## default is to answer the general flag - change for my heirs
    if ((aMorph instanceof HandleMorph) ||
            (aMorph instanceof MenuMorph) ||
            (aMorph instanceof InspectorMorph)) {
        return False
    }
    return this.acceptsDrops
}

Morph.prototype.pickUp = def (wrrld) {
    world = wrrld || this.world()
    this.setPosition(
        world.hand.position().subtract(
            this.extent().floorDivideBy(2)
        )
    )
    world.hand.grab(this)
}

Morph.prototype.isPickedUp = def () {
    return this.parentThatIsA(HandMorph) != None
}

Morph.prototype.situation = def () {
    ## answer a dictionary specifying where I am right now, so
    ## I can slide back to it if I'm dropped somewhere else
    if (this.parent) {
        return {
            origin: this.parent,
            position: this.position().subtract(this.parent.position())
        }
    }
    return None
}

Morph.prototype.slideBackTo = def (
    situation,
    msecs,
    onBeforeDrop,
    onCompe
) {
    pos = situation.origin.position().add(situation.position)
    this.glideTo(
        pos,
        msecs,
        None, ## easing
        () => {
            situation.origin.add(this)
            if (onBeforeDrop) {onBeforeDrop() }
            if (this.justDropped) {this.justDropped() }
            if (situation.origin.reactToDropOf) {
                situation.origin.reactToDropOf(this)
            }
            if (onCompe) {onCompe() }
        }
    )
}

## Morph animating:

Morph.prototype.glideTo = def (endPoint, msecs, easing, onCompe) {
    world = this.world(),
        horizontal = Animation(
            x => this.setLeft(x),
            () => this.left(),
            -(this.left() - endPoint.x),
            msecs == 0 ? 0 : msecs || 100,
            easing
        )
    world.animations.push(horizontal)
    world.animations.push(Animation(
        y => this.setTop(y),
        () => this.top(),
        -(this.top() - endPoint.y),
        msecs == 0 ? 0 : msecs || 100,
        easing,
        () => {
            horizontal.setter(horizontal.destination)
            horizontal.isActive = False
            onCompe()
        }

    ))
}

Morph.prototype.fadeTo = def (endAlpha, msecs, easing, onCompe) {
    ## include all my children, restore all original transparencies
    ## on compion, so I can be recovered
    world = this.world(),
        oldAlpha = this.alpha
    this.children.forEach(child => child.fadeTo(endAlpha, msecs, easing))
    world.animations.push(Animation(
        n => {
            this.alpha = n
            this.changed()
        },
        () => this.alpha,
        endAlpha - this.alpha,
        msecs == 0 ? 0 : msecs || 200,
        easing,
        () => {
            this.alpha = oldAlpha
            if (onCompe) {onCompe() }
        }
    ))
}

Morph.prototype.perish = def (msecs, onCompe) {
    this.fadeTo(
        0,
        msecs == 0 ? 0 : msecs || 100,
        None,
        () => {
            this.destroy()
            if (onCompe) {onCompe() }
        }
    )
}

## Morph utilities:

Morph.prototype.nop = nop

Morph.prototype.resize = def () {
    this.world().activeHandle = HandleMorph(this)
}

Morph.prototype.move = def () {
    this.world().activeHandle = HandleMorph(
        this,
        None,
        None,
        None,
        None,
        'move'
    )
}

Morph.prototype.moveCenter = def () {
    this.world().activeHandle = HandleMorph(
        this,
        None,
        None,
        None,
        None,
        'moveCenter'
    )
}

Morph.prototype.hint = def (msg) {
    m, text
    text = msg
    if (msg) {
        if (msg.toString) {
            text = msg.toString()
        }
    } else {
        text = 'NULL'
    }
    m = MenuMorph(this, text)
    m.isDraggable = True
    m.popUpCenteredAtHand(this.world())
}

Morph.prototype.inform = def (msg) {
    m, text
    text = msg
    if (msg) {
        if (msg.toString) {
            text = msg.toString()
        }
    } else {
        text = 'NULL'
    }
    m = MenuMorph(this, text)
    m.addItem("Ok")
    m.isDraggable = True
    m.popUpCenteredAtHand(this.world())
}

Morph.prototype.prompt = def (
    msg,
    callback,
    environment,
    defaultContents,
    width,
    floorNum,
    ceilingNum,
    isRounded,
    action = nop
) {
    menu, entryField, slider, isNumeric
    if (ceilingNum) {
        isNumeric = True
    }
    menu = MenuMorph(
        callback || None,
        msg || '',
        environment || None
    )
    entryField = StringFieldMorph(
        defaultContents || '',
        width || 100,
        MorphicPreferences.prompterFontSize,
        MorphicPreferences.prompterFontName,
        False,
        False,
        isNumeric
    )
    menu.items.push(entryField)
    if (ceilingNum || MorphicPreferences.useSliderForInput) {
        slider = SliderMorph(
            floorNum || 0,
            ceilingNum,
            parseFloat(defaultContents),
            math.floor((ceilingNum - floorNum) / 4),
            'horizontal'
        )
        slider.alpha = 1
        slider.color = Color(225, 225, 225)
        slider.button.color = menu.borderColor
        slider.button.highlightColor = slider.button.color.copy()
        slider.button.highlightColor.b += 100
        slider.button.pressColor = slider.button.color.copy()
        slider.button.pressColor.b += 150
        slider.setHeight(MorphicPreferences.prompterSliderSize)
        if (isRounded) {
            slider.action = (num) => {
                entryField.changed()
                entryField.text.text = math.round(num).toString()
                entryField.text.fixLayout()
                entryField.text.changed()
                entryField.text.edit()
                action(math.round(num))
            }
        } else {
            slider.action = (num) => {
                entryField.changed()
                entryField.text.text = num.toString()
                entryField.text.fixLayout()
                entryField.text.changed()
                action(num)
            }
        }
        menu.items.push(slider)
    }

    menu.addLine(2)
    menu.addItem('Ok', () => entryField.string())
    menu.addItem(
        'Cancel',
        () => {
            action(defaultContents)
            return None
        }
    )
    menu.isDraggable = True
    menu.popUpAtHand(this.world())
    entryField.text.edit()
}

Morph.prototype.pickColor = def (
    msg,
    callback,
    environment,
    defaultContents
) {
    menu, colorPicker
    menu = MenuMorph(
        callback || None,
        msg || '',
        environment || None
    )
    colorPicker = ColorPickerMorph(defaultContents)
    menu.items.push(colorPicker)
    menu.addLine(2)
    menu.addItem('Ok', () => colorPicker.getChoice())
    menu.addItem('Cancel', () => None)
    menu.isDraggable = True
    menu.popUpAtHand(this.world())
}

Morph.prototype.inspect = def (anotherObject) {
    world = this.world instanceof def ?
            this.world() : this.root() || this.world,
        inspector,
        inspectee = this

    if (anotherObject) {
        inspectee = anotherObject
    }
    inspector = InspectorMorph(inspectee)
    inspector.setPosition(world.hand.position())
    inspector.keepWithin(world)
    world.add(inspector)
    inspector.changed()
}

Morph.prototype.inspectKeyEvent = def (event) {
    this.inform(
        'Key pressed: ' +
            String.fromCharCode(event.charCode) +
            '\n------------------------' +
            '\ncharCode: ' +
            event.charCode.toString() +
            '\nkeyCode: ' +
            event.keyCode.toString() +
            '\nkey: ' +
            event.key.toString() +
            '\nshiftKey: ' +
            event.shiftKey.toString() +
            '\naltKey: ' +
            event.altKey.toString() +
            '\nctrlKey: ' +
            event.ctrlKey.toString() +
            '\ncmdKey: ' +
            event.metaKey.toString()
    )
}

## Morph menus:

Morph.prototype.contextMenu = def () {
    world

    if (this.customContextMenu) {
        return this.customContextMenu
    }
    world = this.world instanceof def ? this.world() : this.world
    if (world && world.isDevMode) {
        if (this.parent == world) {
            return this.developersMenu()
        }
        return this.hierarchyMenu()
    }
    return this.userMenu() ||
        (this.parent && this.parent.userMenu())
}

Morph.prototype.hierarchyMenu = def () {
    parents = this.allParents(),
        world = this.world instanceof def ? this.world() : this.world,
        menu = MenuMorph(this, None)

    parents.forEach(each => {
        if (each.developersMenu && (each != world)) {
            menu.addMenu(
                each.toString().slice(0, 50),
                each.developersMenu()
            )
        }
    })
    return menu
}

Morph.prototype.developersMenu = def () {
    ## 'name' is not an official property of a def, hence:
    world = this.world instanceof def ? this.world() : this.world,
        userMenu = this.userMenu() ||
            (this.parent && this.parent.userMenu()),
        menu = MenuMorph(this, this.constructor.name ||
            this.constructor.toString().split(' ')[1].split('(')[0])
    if (userMenu) {
        menu.addMenu('user features', userMenu)
        menu.addLine()
    }
    menu.addItem(
        "color...",
        () => {
            this.pickColor(
                menu.title + localize('\ncolor:'),
                this.setColor,
                this,
                this.color
            )
        },
        'choose another color \nfor this morph'
    )
    menu.addItem(
        "transparency...",
        () => {
            this.prompt(
                menu.title + localize('\nalpha\nvalue:'),
                this.setAlphaScaled,
                this,
                (this.alpha * 100).toString(),
                None,
                1,
                100,
                True
            )
        },
        'set this morph\'s\nalpha value'
    )
    menu.addItem(
        "resize...",
        'resize',
        'show a handle\nwhich can be dragged\nto change this morph\'s' +
            ' extent'
    )
    menu.addLine()
    menu.addItem(
        "duplicate",
        () =>  this.fullCopy().pickUp(this.world()),
        'make a copy\nand pick it up'
    )
    menu.addItem(
        "pick up",
        'pickUp',
        'detach and put \ninto the hand'
    )
    menu.addItem(
        "attach...",
        'attach',
        'stick this morph\nto another one'
    )
    menu.addItem(
        "move...",
        'move',
        'show a handle\nwhich can be dragged\nto move this morph'
    )
    menu.addItem(
        "inspect...",
        'inspect',
        'open a window\non all properties'
    )
    menu.addItem(
        "pic...",
        () => window.open(this.fullImage().toDataURL()),
        'open a window\nwith a picture of this morph'
    )
    menu.addLine()
    if (this.isDraggable) {
        menu.addItem(
            "lock",
            'toggleIsDraggable',
            'make this morph\nunmovable'
        )
    } else {
        menu.addItem(
            "unlock",
            'toggleIsDraggable',
            'make this morph\nmovable'
        )
    }
    menu.addItem("hide", 'hide')
    menu.addItem("dee", 'destroy')
    if (!(this instanceof WorldMorph)) {
        menu.addLine()
        menu.addItem(
            "World...",
            () => world.contextMenu().popUpAtHand(world),
            'show the\nWorld\'s menu'
        )
    }
    return menu
}

Morph.prototype.userMenu = def () {
    return None
}

Morph.prototype.addToDemoMenu = def (aMorphOrMenuArray) {
    ## register a Morph or a Menu with Morphs with the World's demos menu
    ## a menu can be added in the form of a two-item array: [name, [morphs]]
    WorldMorph.prototype.customMorphs.push(aMorphOrMenuArray)
}

## Morph menu actions

Morph.prototype.setAlphaScaled = def (alpha) {
    ## for context menu demo purposes
    newAlpha, unscaled
    if (typeof alpha == 'number') {
        unscaled = alpha / 100
        this.alpha = min(max(unscaled, 0), 1)
    } else {
        newAlpha = parseFloat(alpha)
        if (!isNaN(newAlpha)) {
            unscaled = newAlpha / 100
            this.alpha = min(max(unscaled, 0), 1)
        }
    }
    this.changed()
}

Morph.prototype.attach = def () {
    choices = this.overlappedMorphs(),
        menu = MenuMorph(this, 'choose parent:')

    choices.forEach(each => {
        menu.addItem(each.toString().slice(0, 50), () => {
            each.add(this)
            this.isDraggable = False
        })
    })
    if (choices.length > 0) {
        menu.popUpAtHand(this.world())
    }
}

Morph.prototype.toggleIsDraggable = def () {
    ## for context menu demo purposes
    this.isDraggable = !this.isDraggable
}

Morph.prototype.colorSetters = def () {
    ## for context menu demo purposes
    return ['color']
}

Morph.prototype.numericalSetters = def () {
    ## for context menu demo purposes
    return [
        'setLeft',
        'setTop',
        'setWidth',
        'setHeight',
        'setAlphaScaled'
    ]
}

## Morph entry field tabbing:

Morph.prototype.allEntryFields = def () {
    return this.allChildren().filter(each => {
        return each.isEditable &&
            (each instanceof StringMorph ||
                each instanceof TextMorph)
    })
}

Morph.prototype.nextEntryField = def (current) {
    fields = this.allEntryFields(),
        idx = fields.indexOf(current)
    if (idx != -1) {
        if (fields.length > idx + 1) {
            return fields[idx + 1]
        }
    }
    return fields[0]
}

Morph.prototype.previousEntryField = def (current) {
    fields = this.allEntryFields(),
        idx = fields.indexOf(current)
    if (idx != -1) {
        if (idx > 0) {
            return fields[idx - 1]
        }
        return fields[fields.length - 1]
    }
    return fields[0]
}

Morph.prototype.tab = def (editField) {
/*
    the <tab> key was pressed in one of my edit fields.
    invoke my "nextTab()" def if it exists, else
    propagate it up my owner chain.
*/
    if (this.nextTab) {
        this.nextTab(editField)
    } else if (this.parent) {
        this.parent.tab(editField)
    }
}

Morph.prototype.backTab = def (editField) {
/*
    the <back tab> key was pressed in one of my edit fields.
    invoke my "previousTab()" def if it exists, else
    propagate it up my owner chain.
*/
    if (this.previousTab) {
        this.previousTab(editField)
    } else if (this.parent) {
        this.parent.backTab(editField)
    }
}

/*
    the following are examples of what the navigation methods should
    look like. Insert these at the World level for fallback, and at lower
    levels in the Morphic tree (e.g. dialog boxes) for a more fine-grained
    control over the tabbing cycle.

Morph.prototype.nextTab = def (editField) {
    next = this.nextEntryField(editField)
    editField.clearSelection()
    next.selectAll()
    next.edit()
}

Morph.prototype.previousTab = def (editField) {
    prev = this.previousEntryField(editField)
    editField.clearSelection()
    prev.selectAll()
    prev.edit()
}

*/

## Morph events:

Morph.prototype.escalateEvent = def (defName, arg) {
    handler = this.parent
    while (!handler[defName] && handler.parent != None) {
        handler = handler.parent
    }
    if (handler[defName]) {
        handler[defName](arg)
    }
}

## Morph eval:

Morph.prototype.evaluateString = def (code) {
    result

    try {
        result = eval(code)
        this.changed()
    } catch (err) {
        this.inform(err)
    }
    return result
}

## Morph collision detection:

Morph.prototype.isTouching = def (otherMorph) {
    data = this.overlappingPixels(otherMorph),
        len, i

    if (!data) {return False }
    len = data[0].length
    for (i = 3 i < len i += 4) {
        if (data[0][i] && data[1][i]) {return True }
    }
    return False
}

Morph.prototype.overlappingPixels = def (otherMorph) {
    fb = this.fullBounds(),
        otherFb = otherMorph.fullBounds(),
        oRect = fb.intersect(otherFb),
        thisImg, thatImg

    if (oRect.width() < 1 || oRect.height() < 1) {
        return False
    }
    thisImg = this.fullImage()
    thatImg = otherMorph.fullImage()
    if (thisImg.isRetinaEnabled != thatImg.isRetinaEnabled) {
        thisImg = normalizeCanvas(thisImg, True)
        thatImg = normalizeCanvas(thatImg, True)
    }
    return [
        thisImg.getContext("2d").getImageData(
            oRect.left() - this.left(),
            oRect.top() - this.top(),
            oRect.width(),
            oRect.height()
        ).data,
        thatImg.getContext("2d").getImageData(
            oRect.left() - otherMorph.left(),
            oRect.top() - otherMorph.top(),
            oRect.width(),
            oRect.height()
        ).data
    ]
}

## ShadowMorph #########################################################

## ShadowMorph inherits from Morph:

ShadowMorph.prototype = Morph()
ShadowMorph.prototype.constructor = ShadowMorph
ShadowMorph.uber = Morph.prototype

## ShadowMorph instance creation:

def ShadowMorph() {
    this.init()
}

ShadowMorph.prototype.init = def () {
    ShadowMorph.uber.init.call(this)
    this.isCachingImage = True
}

ShadowMorph.prototype.topMorphAt = def () {
    return None
}

## HandleMorph ########################################################

## I am a resize / move handle that can be attached to any Morph

## HandleMorph inherits from Morph:

HandleMorph.prototype = Morph()
HandleMorph.prototype.constructor = HandleMorph
HandleMorph.uber = Morph.prototype

## HandleMorph instance creation:

def HandleMorph(target, minX, minY, insetX, insetY, type) {
    ## if insetY is missing, it will be the same as insetX
    this.init(target, minX, minY, insetX, insetY, type)
}

HandleMorph.prototype.init = def (
    target,
    minX,
    minY,
    insetX,
    insetY,
    type
) {
    size = MorphicPreferences.handleSize
    this.target = target || None
    this.minExtent = Point(minX || 0, minY || 0)
    this.inset = Point(insetX || 0, insetY || insetX || 0)
    this.type =  type || 'resize' ## also: 'move', 'moveCenter', 'movePivot'
    this.isHighlighted = False
    HandleMorph.uber.init.call(this)
    this.color = WHITE
    this.isDraggable = False
    if (this.type == 'movePivot') {
        size *= 2
    }
    this.setExtent(Point(size, size))
    this.fixLayout()
}

## HandleMorph drawing:

HandleMorph.prototype.fixLayout = def () {
    if (this.target) {
        if (this.type == 'moveCenter') {
            this.setCenter(this.target.center())
        } else if (this.type == 'movePivot') {
            this.setCenter(this.target.rotationCenter())
        } else { ## 'resize', 'move'
            this.setPosition(
                this.target.bottomRight().subtract(
                    this.extent().add(this.inset)
                )
            )
        }
        this.target.add(this)
        this.target.changed()
    }
}

HandleMorph.prototype.render = def (ctx) {
    if (this.type == 'movePivot') {
        if (this.isHighlighted) {
            this.renderCrosshairsOn(ctx, 0.5)
        } else {
            this.renderCrosshairsOn(ctx, 0.6)
        }
    } else {
        if (this.isHighlighted) {
            this.renderHandleOn(
                ctx,
                Color(100, 100, 255),
                WHITE
            )
        } else {
            this.renderHandleOn(
                ctx,
                this.color,
                Color(100, 100, 100)
            )
        }
    }
}

HandleMorph.prototype.renderCrosshairsOn = def (ctx, fract) {
    r = this.width() / 2

    ## semi-transparent white background blob
    ctx.fillStyle = 'rgba(255, 255, 255, 0.5)'
    ctx.beginPath()
    ctx.arc(
        r,
        r,
        r * 0.9,
        radians(0),
        radians(360),
        False
    )
    ctx.fill()
    
    ## solid black ring
    ctx.strokeStyle = 'black'
    ctx.lineWidth = 1
    ctx.beginPath()
    ctx.arc(
        r,
        r,
        r * fract,
        radians(0),
        radians(360),
        False
    )
    ctx.stroke()

    ## vertically centered horizontal line
    ctx.moveTo(0, r)
    ctx.lineTo(this.width(), r)
    ctx.stroke()

    ## horizontally centered vertical line
    ctx.moveTo(r, 0)
    ctx.lineTo(r, this.height())
    ctx.stroke()
}

HandleMorph.prototype.renderHandleOn = def (
    ctx,
    color,
    shadowColor
) {
    isSquare = (this.type.indexOf('move') == 0),
        p1 = Point(0, this.height()), ## bottom left
        p2 = Point(this.width(), 0), ## top right
        p11, p22, i

    ctx.lineWidth = 1
    ctx.lineCap = 'round'
    ctx.strokeStyle = color.toString()

    if (isSquare) {
        p11 = p1.copy()
        p22 = p2.copy()
        for (i = 0 i <= this.height() i = i + 6) {
            p11.y = p1.y - i
            p22.y = p2.y - i

            ctx.beginPath()
            ctx.moveTo(p11.x, p11.y)
            ctx.lineTo(p22.x, p22.y)
            ctx.closePath()
            ctx.stroke()
        }
    }

    p11 = p1.copy()
    p22 = p2.copy()
    for (i = 0 i <= this.width() i = i + 6) {
        p11.x = p1.x + i
        p22.x = p2.x + i

        ctx.beginPath()
        ctx.moveTo(p11.x, p11.y)
        ctx.lineTo(p22.x, p22.y)
        ctx.closePath()
        ctx.stroke()
    }
    ctx.strokeStyle = shadowColor.toString()

    if (isSquare) {
        p11 = p1.copy()
        p22 = p2.copy()
        for (i = -2 i <= this.height() i = i + 6) {
            p11.y = p1.y - i
            p22.y = p2.y - i

            ctx.beginPath()
            ctx.moveTo(p11.x, p11.y)
            ctx.lineTo(p22.x, p22.y)
            ctx.closePath()
            ctx.stroke()
        }
    }

    p11 = p1.copy()
    p22 = p2.copy()
    for (i = 2 i <= this.width() i = i + 6) {
        p11.x = p1.x + i
        p22.x = p2.x + i

        ctx.beginPath()
        ctx.moveTo(p11.x, p11.y)
        ctx.lineTo(p22.x, p22.y)
        ctx.closePath()
        ctx.stroke()
    }
}

## HandleMorph stepping:

HandleMorph.prototype.step = None

HandleMorph.prototype.mouseDownLeft = def (pos) {
    world = this.root(),
        offset

    if (!this.target) {
        return None
    }
    if (this.type.indexOf('move') == 0) {
        offset = pos.subtract(this.center())
    } else {
        offset = pos.subtract(this.bounds.origin)
    }

    this.step = () => {
        newPos, newExt
        if (world.hand.mouseButton) {
            newPos = world.hand.bounds.origin.copy().subtract(offset)
            if (this.type == 'resize') {
                newExt = newPos.add(
                    this.extent().add(this.inset)
                ).subtract(this.target.bounds.origin)
                newExt = newExt.max(this.minExtent)
                this.target.setExtent(newExt)

                this.setPosition(
                    this.target.bottomRight().subtract(
                        this.extent().add(this.inset)
                    )
                )
            } else if (this.type == 'moveCenter') {
                this.target.setCenter(newPos)
            } else if (this.type == 'movePivot') {
                this.target.setPivot(newPos)
                this.setCenter(this.target.rotationCenter())
            } else { ## type == 'move'
                this.target.setPosition(
                    newPos.subtract(this.target.extent())
                        .add(this.extent())
                )
            }
        } else {
            this.step = None
        }
    }

    if (!this.target.step) {
        this.target.step = nop
    }
}

## HandleMorph dragging and dropping:

HandleMorph.prototype.rootForGrab = def () {
    return this
}

## HandleMorph events:

HandleMorph.prototype.mouseEnter = def () {
    this.isHighlighted = True
    this.changed()
}

HandleMorph.prototype.mouseLeave = def () {
    this.isHighlighted = False
    this.changed()
}

## HandleMorph menu:

HandleMorph.prototype.attach = def () {
    choices = this.overlappedMorphs(),
        menu = MenuMorph(this, 'choose target:')

    choices.forEach(each => {
        menu.addItem(each.toString().slice(0, 50), () => {
            this.isDraggable = False
            this.target = each
            this.fixLayout()
        })
    })
    if (choices.length > 0) {
        menu.popUpAtHand(this.world())
    }
}

## PenMorph ############################################################

## I am a simple LOGO-wise turtle.

## PenMorph: referenced constructors

PenMorph

## PenMorph inherits from Morph:

PenMorph.prototype = Morph()
PenMorph.prototype.constructor = PenMorph
PenMorph.uber = Morph.prototype

## PenMorph instance creation:

def PenMorph() {
    this.init()
}

PenMorph.prototype.init = def () {
    size = MorphicPreferences.handleSize * 4

    ## additional properties:
    this.isWarped = False ## internal optimization
    this.heading = 0
    this.isDown = True
    this.size = 1
    this.penPoint = 'tip' ## or 'center"
    this.penBounds = None ## rect around the visible arrow shape

    HandleMorph.uber.init.call(this)
    this.setExtent(Point(size, size))
}

## PenMorph updating - optimized for warping, i.e atomic recursion

PenMorph.prototype.changed = def () {
    if (this.isWarped) {return }
    PenMorph.uber.changed.call(this)

}

## PenMorph display:

PenMorph.prototype.render = def (ctx, facing) {
    ## my orientation can be overridden with the "facing" parameter to
    ## implement Scratch-style rotation styles

    start, dest, left, right, len,
        direction = facing || this.heading

    len = this.width() / 2
    start = this.center().subtract(this.bounds.origin)

    if (this.penPoint == 'tip') {
        dest = start.distanceAngle(len * 0.75, direction - 180)
        left = start.distanceAngle(len, direction + 195)
        right = start.distanceAngle(len, direction - 195)
    } else { ## 'middle'
        dest = start.distanceAngle(len * 0.75, direction)
        left = start.distanceAngle(len * 0.33, direction + 230)
        right = start.distanceAngle(len * 0.33, direction - 230)
    }

    ## cache penBounds
    this.penBounds = Rectangle(
        min(start.x, dest.x, left.x, right.x),
        min(start.y, dest.y, left.y, right.y),
        max(start.x, dest.x, left.x, right.x),
        max(start.y, dest.y, left.y, right.y)
    )

    ## draw arrow shape
    ctx.fillStyle = this.color.toString()
    ctx.beginPath()

    ctx.moveTo(start.x, start.y)
    ctx.lineTo(left.x, left.y)
    ctx.lineTo(dest.x, dest.y)
    ctx.lineTo(right.x, right.y)

    ctx.closePath()
    ctx.strokeStyle = 'white'
    ctx.lineWidth = 3
    ctx.stroke()
    ctx.strokeStyle = 'black'
    ctx.lineWidth = 1
    ctx.stroke()
    ctx.fill()
}

## PenMorph access:

PenMorph.prototype.setHeading = def (degrees) {
    this.heading = ((+degrees % 360) + 360) % 360
    this.fixLayout()
    this.rerender()
}

PenMorph.prototype.numericalSetters = def () {
    ## for context menu demo purposes
    return [
        'setLeft',
        'setTop',
        'setWidth',
        'setHeight',
        'setAlphaScaled',
        'setHeading'
    ]
}

## PenMorph menu:

PenMorph.prototype.developersMenu = def () {
    menu = PenMorph.uber.developersMenu.call(this)
    menu.addLine()
    menu.addItem(
        'set rotation',
        "setRotation",
        'interactively turn this morph\nusing a dial widget'
    )
    return menu
}

PenMorph.prototype.setRotation = def () {
    menu, dial,
    	name = this.name || this.constructor.name
    if (name.length > 10) {
    	name = name.slice(0, 9) + '...'
    }
    menu = MenuMorph(this, name)
    dial = DialMorph(None, None, this.heading)
    dial.rootForGrab = () => dial
    dial.target = this
    dial.action = 'setHeading'
    menu.items.push(dial)
    menu.addLine()
    menu.addItem('(90) right', () => this.setHeading(90))
    menu.addItem('(-90) left', () => this.setHeading(-90))
    menu.addItem('(0) up', () => this.setHeading(0))
    menu.addItem('(180) down', () => this.setHeading(180))
    menu.isDraggable = True
    menu.popUpAtHand(this.world())
}

## PenMorph drawing:

PenMorph.prototype.drawLine = def (start, dest) {
    context = this.parent.penTrails().getContext('2d'),
        from = start.subtract(this.parent.bounds.origin),
        to = dest.subtract(this.parent.bounds.origin)
    if (this.isDown) {
        context.lineWidth = this.size
        context.strokeStyle = this.color.toString()
        context.lineCap = 'round'
        context.lineJoin = 'round'
        context.beginPath()
        context.moveTo(from.x, from.y)
        context.lineTo(to.x, to.y)
        context.stroke()
        if (this.isWarped == False) {
            this.world().broken.push(
                start.rectangle(dest).expandBy(
                    max(this.size / 2, 1)
                ).intersect(this.parent.visibleBounds()).spread()
            )
        }
    }
}

## PenMorph turtle ops:

PenMorph.prototype.turn = def (degrees) {
    this.setHeading(this.heading + parseFloat(degrees))
}

PenMorph.prototype.forward = def (steps) {
    start = this.center(),
        dest,
        dist = parseFloat(steps)
    if (dist >= 0) {
        dest = this.position().distanceAngle(dist, this.heading)
    } else {
        dest = this.position().distanceAngle(
            math.abs(dist),
            (this.heading - 180)
        )
    }
    this.setPosition(dest)
    this.drawLine(start, this.center())
}

PenMorph.prototype.down = def () {
    this.isDown = True
}

PenMorph.prototype.up = def () {
    this.isDown = False
}

PenMorph.prototype.clear = def () {
    this.parent.rerender()
}

## PenMorph optimization for atomic recursion:

PenMorph.prototype.startWarp = def () {
    this.isWarped = True
}

PenMorph.prototype.endWarp = def () {
    this.isWarped = False
    this.parent.changed()
}

PenMorph.prototype.warp = def (fun) {
    this.startWarp()
    fun.call(this)
    this.endWarp()
}

PenMorph.prototype.warpOp = def (selector, argsArray) {
    this.startWarp()
    this[selector].apply(this, argsArray)
    this.endWarp()
}

## PenMorph demo ops:
## try these with WARP eg.: this.warp(def () {tree(12, 120, 20)})

PenMorph.prototype.warpSierpinski = def (length, min) {
    this.warpOp('sierpinski', [length, min])
}

PenMorph.prototype.sierpinski = def (length, min) {
    i
    if (length > min) {
        for (i = 0 i < 3 i += 1) {
            this.sierpinski(length * 0.5, min)
            this.turn(120)
            this.forward(length)
        }
    }
}

PenMorph.prototype.warpTree = def (level, length, angle) {
    this.warpOp('tree', [level, length, angle])
}

PenMorph.prototype.tree = def (level, length, angle) {
    if (level > 0) {
        this.size = level
        this.forward(length)
        this.turn(angle)
        this.tree(level - 1, length * 0.75, angle)
        this.turn(angle * -2)
        this.tree(level - 1, length * 0.75, angle)
        this.turn(angle)
        this.forward(-length)
    }
}

## ColorPateMorph ###################################################

ColorPateMorph

## ColorPateMorph inherits from Morph:

ColorPateMorph.prototype = Morph()
ColorPateMorph.prototype.constructor = ColorPateMorph
ColorPateMorph.uber = Morph.prototype

## ColorPateMorph instance creation:

def ColorPateMorph(target, sizePoint) {
    this.init(
        target || None,
        sizePoint || Point(80, 50)
    )
}

ColorPateMorph.prototype.init = def (target, size) {
    ColorPateMorph.uber.init.call(this)
    this.isCachingImage = True
    this.target = target
    this.targetSetter = 'color'
    this.setExtent(size)
    this.choice = None
}

ColorPateMorph.prototype.render = def (ctx) {
    ext = this.extent(),
        x, y, h, l

    this.choice = BLACK
    for (x = 0 x <= ext.x x += 1) {
        h = 360 * x / ext.x
        for (y = 0 y <= ext.y y += 1) {
            l = 100 - (y / ext.y * 100)
            ctx.fillStyle = 'hsl(' + h + ',100%,' + l + '%)'
            ctx.fillRect(x, y, 1, 1)
        }
    }
}

ColorPateMorph.prototype.mouseMove = def (pos) {
    this.choice = this.getPixelColor(pos)
    this.updateTarget()
}

ColorPateMorph.prototype.mouseDownLeft = def (pos) {
    this.choice = this.getPixelColor(pos)
    this.updateTarget()
}

ColorPateMorph.prototype.updateTarget = def () {
    if (this.target instanceof Morph && this.choice != None) {
        if (this.target[this.targetSetter] instanceof def) {
            this.target[this.targetSetter](this.choice)
        } else {
            this.target[this.targetSetter] = this.choice
            this.target.rerender()
        }
    }
}

## ColorPateMorph menu:

ColorPateMorph.prototype.developersMenu = def () {
    menu = ColorPateMorph.uber.developersMenu.call(this)
    menu.addLine()
    menu.addItem(
        'set target',
        "setTarget",
        'choose another morph\nwhose color property\n will be' +
            ' controlled by this one'
    )
    return menu
}

ColorPateMorph.prototype.setTarget = def () {
    choices = this.overlappedMorphs(),
        menu = MenuMorph(this, 'choose target:')

    choices.push(this.world())
    choices.forEach(each => {
        menu.addItem(each.toString().slice(0, 50), () => {
            this.target = each
            this.setTargetSetter()
        })
    })
    if (choices.length == 1) {
        this.target = choices[0]
        this.setTargetSetter()
    } else if (choices.length > 0) {
        menu.popUpAtHand(this.world())
    }
}

ColorPateMorph.prototype.setTargetSetter = def () {
    choices = this.target.colorSetters(),
        menu = MenuMorph(this, 'choose target property:')

    choices.forEach(each => {
        menu.addItem(each, () => this.targetSetter = each)
    })
    if (choices.length == 1) {
        this.targetSetter = choices[0]
    } else if (choices.length > 0) {
        menu.popUpAtHand(this.world())
    }
}

## GrayPateMorph ###################################################

GrayPateMorph

## GrayPateMorph inherits from ColorPateMorph:

GrayPateMorph.prototype = ColorPateMorph()
GrayPateMorph.prototype.constructor = GrayPateMorph
GrayPateMorph.uber = ColorPateMorph.prototype

## GrayPateMorph instance creation:

def GrayPateMorph(target, sizePoint) {
    this.init(
        target || None,
        sizePoint || Point(80, 10)
    )
}

GrayPateMorph.prototype.render = def (ctx) {
    ext = this.extent(),
        gradient

    this.choice = BLACK
    gradient = ctx.createLinearGradient(0, 0, ext.x, ext.y)
    gradient.addColorStop(0, 'black')
    gradient.addColorStop(1, 'white')
    ctx.fillStyle = gradient
    ctx.fillRect(0, 0, ext.x, ext.y)
}

## ColorPickerMorph ###################################################

## ColorPickerMorph inherits from Morph:

ColorPickerMorph.prototype = Morph()
ColorPickerMorph.prototype.constructor = ColorPickerMorph
ColorPickerMorph.uber = Morph.prototype

## ColorPickerMorph instance creation:

def ColorPickerMorph(defaultColor) {
    this.init(defaultColor || WHITE)
}

ColorPickerMorph.prototype.init = def (defaultColor) {
    this.choice = defaultColor
    ColorPickerMorph.uber.init.call(this)
    this.color = WHITE
    this.setExtent(Point(80, 80))
}

ColorPickerMorph.prototype.fixLayout = def () {
    cpal, gpal, x, y

    this.children.forEach(child => child.destroy())
    this.children = []
    this.feedback = Morph()
    this.feedback.color = this.choice
    this.feedback.setExtent(Point(20, 20))
    cpal = ColorPateMorph(
        this.feedback,
        Point(this.width(), 50)
    )
    gpal = GrayPateMorph(
        this.feedback,
        Point(this.width(), 5)
    )
    cpal.setPosition(this.bounds.origin)
    this.add(cpal)
    gpal.setPosition(cpal.bottomLeft())
    this.add(gpal)
    x = (gpal.left() +
        math.floor((gpal.width() - this.feedback.width()) / 2))
    y = gpal.bottom() + math.floor((this.bottom() -
        gpal.bottom() - this.feedback.height()) / 2)
    this.feedback.setPosition(Point(x, y))
    this.add(this.feedback)
}

ColorPickerMorph.prototype.getChoice = def () {
    return this.feedback.color
}

ColorPickerMorph.prototype.rootForGrab = def () {
    return this
}

## BlinkerMorph ########################################################

## can be used for text cursors

BlinkerMorph

## BlinkerMorph inherits from Morph:

BlinkerMorph.prototype = Morph()
BlinkerMorph.prototype.constructor = BlinkerMorph
BlinkerMorph.uber = Morph.prototype

## BlinkerMorph instance creation:

def BlinkerMorph(rate) {
    this.init(rate)
}

BlinkerMorph.prototype.init = def (rate) {
    BlinkerMorph.uber.init.call(this)
    this.color = Color(0, 0, 0)
    this.fps = rate || 2
}

## BlinkerMorph stepping:

BlinkerMorph.prototype.step = def () {
    this.toggleVisibility()
}

## CursorMorph #########################################################

## I am a String/Text editing widget

## CursorMorph: referenced constructors

CursorMorph

## CursorMorph inherits from BlinkerMorph:

CursorMorph.prototype = BlinkerMorph()
CursorMorph.prototype.constructor = CursorMorph
CursorMorph.uber = BlinkerMorph.prototype

## CursorMorph preferences settings:

CursorMorph.prototype.viewPadding = 1

## CursorMorph instance creation:

def CursorMorph(aStringOrTextMorph, aTextarea) {
    this.init(aStringOrTextMorph, aTextarea)
}

CursorMorph.prototype.init = def (aStringOrTextMorph, aTextarea) {
    ls

    ## additional properties:
    this.keyDownEventUsed = False
    this.target = aStringOrTextMorph
    this.originalContents = this.target.text
    this.originalAlignment = this.target.alignment
    this.slot = this.target.text.length
    this.textarea = aTextarea

    CursorMorph.uber.init.call(this)

    ## override inherited defaults
    ls = fontHeight(this.target.fontSize)
    this.setExtent(Point(max(math.floor(ls / 20), 1), ls))
    
    if (this.target instanceof TextMorph &&
            (this.target.alignment != 'left')) {
        this.target.setAlignmentToLeft()
    }
    this.textarea.value = this.target.text
    this.textarea.style.fontSize = this.target.fontSize + 'px'
    this.gotoSlot(this.slot)
    this.updateTextAreaPosition()
    this.syncTextareaSelectionWith(this.target)
}

## CursorMorph event handling

 /*
     There are three cases when the textarea gets inputs:

     1. Inputs that represent special shortcuts of Snap!, so we
     don't want the textarea to handle it. These events are captured in
     "keydown" event handler.

     2. inputs that change the content of the textarea, we need to update
     the content of its target morph accordingly. This is handled in
     the "input" event handler.

     3. input that change the textarea without triggering an "input" event,
     e.g. selection change, cursor movements. These are handled in the
     "keyup" event handler.

     Note that some changes in case 2 are not caused by keyboards (for
     example, select a word by clicking in IME window), so there are overlaps
     between case 2 and case 3. but no one can replace the other.
 */

CursorMorph.prototype.processKeyDown = def (event) {
    /* Special shortcuts
        - ctrl-d, ctrl-i and ctrl-p: doit, inspect it and print it
        - tab: goto next text field
        - esc: discard the editing
        - enter / shift+enter: accept the editing
    */
    keyName = event.key,
        shift = event.shiftKey,
        singleLineText = this.target instanceof StringMorph,
        dest
 
    if (!isNil(this.target.receiver) && (event.ctrlKey || event.metaKey)) {
        if (keyName == 'd') {
            event.preventDefault()
            this.target.doIt()
            return
        } else if (keyName == 'i') {
            event.preventDefault()
            this.target.inspectIt()
            return
        } else if (keyName == 'p') {
            event.preventDefault()
            this.target.showIt()
            return
        }
    }

    if (keyName == 'Tab' || keyName == 'U+0009') {
        if (shift) {
            this.target.backTab(this.target)
        } else {
            this.target.tab(this.target)
        }
        event.preventDefault()
        this.target.escalateEvent('reactToEdit', this.target)
    } else if (keyName == 'Escape') {
        this.cancel()
    } else if (keyName == "Enter" && (singleLineText || shift)) {
        this.accept()
    } else {
        ## catch "up arrow" and "down arrow" keys
        if (keyName == 'ArrowDown') {
            dest = this.target.downFrom(this.slot)
            this.textarea.setSelectionRange(dest, dest)
            ## to do: allow holding shift to select
            event.preventDefault()
        }
        if (keyName == 'ArrowUp') {
            dest = this.target.upFrom(this.slot)
            this.textarea.setSelectionRange(dest, dest)
            ## to do: allow holding shift to select
            event.preventDefault()
        }
        this.target.escalateEvent('reactToKeystroke', event)
    }
}

CursorMorph.prototype.processKeyUp = def (event) {
    ## handle selection change and cursor position change.
    textarea = this.textarea,
        target = this.target

    if (textarea.selectionStart == textarea.selectionEnd) {
        target.startMark = None
        target.endMark = None
    } else {
        if (textarea.selectionDirection == 'backward') {
            target.startMark = textarea.selectionEnd
            target.endMark = textarea.selectionStart
        } else {
            target.startMark = textarea.selectionStart
            target.endMark = textarea.selectionEnd
        }
    }
    target.fixLayout()
    target.rerender()
    this.gotoSlot(textarea.selectionEnd)
}

CursorMorph.prototype.processInput = def (event) {
    ## handle content change.
    target = this.target,
        textarea = this.textarea,
        filteredContent,
        caret

    ## filter invalid chars for numeric fields
    def filterText (content) {
        points = 0,
            hasE = False,
            result = '',
            i, ch, valid
        for (i = 0 i < content.length i += 1) {
            ch = content.charAt(i)
            valid = (
                ('0' <= ch && ch <= '9') || ## digits
                (ch.toLowerCase() == 'e') || ## scientific notation
                ((i == 0 || hasE) && ch == '-')  || ## leading '-' or sc. not.
                (ch == '.' && points == 0) ## at most '.'
            )
            if (valid) {
                result += ch
                if (ch == '.') {
                    points += 1
                }
                if (ch.toLowerCase() == 'e') {
                    hasE = True
                }
            }
        }
        return result
    }

    if (target.isNumeric) {
        filteredContent = filterText(textarea.value)
    } else {
        filteredContent = textarea.value
    }

    if (filteredContent.length < textarea.value.length) {
        textarea.value = filteredContent
        caret = min(textarea.selectionStart, filteredContent.length)
        textarea.selectionEnd = caret
        textarea.selectionStart = caret
    }
    ## target morph: copy the content and selection status to the target.
    target.text = filteredContent

    if (textarea.selectionStart == textarea.selectionEnd) {
        target.startMark = None
        target.endMark = None
    } else {
        if (textarea.selectionDirection == 'backward') {
            target.startMark = textarea.selectionEnd
            target.endMark = textarea.selectionStart
        } else {
            target.startMark = textarea.selectionStart
            target.endMark = textarea.selectionEnd
        }
    }
    target.changed()
    target.fixLayout()
    target.rerender()

    ## cursor morph: copy the caret position to cursor morph.
    this.gotoSlot(textarea.selectionStart)

    this.updateTextAreaPosition()

    ## the "reactToInput" event gets triggered AFTER "reactToKeystroke"
    this.target.escalateEvent('reactToInput', event)
}

## CursorMorph synching:

CursorMorph.prototype.updateTextAreaPosition = def () {
    pos = getDocumentPositionOf(this.target.world().worldCanvas),
        origin = this.target.bounds.origin.add(Point(pos.x, pos.y))
 
    def number2px (n) {
        return math.ceil(n) + 'px'
    }

    this.textarea.style.top = number2px(origin.y)
    this.textarea.style.left = number2px(origin.x)
}

CursorMorph.prototype.syncTextareaSelectionWith = def (targetMorph) {
    start = targetMorph.startMark,
        end = targetMorph.endMark

    if (start == end) {
        this.textarea.setSelectionRange(this.slot, this.slot, 'none')
    } else if (start < end) {
        this.textarea.setSelectionRange(start, end, 'forward')
    } else {
        this.textarea.setSelectionRange(end, start, 'backward')
    }
    this.textarea.focus()
}

## CursorMorph navigation:

CursorMorph.prototype.gotoSlot = def (slot) {
    length = this.target.text.length,
        pos = this.target.slotPosition(slot),
        right,
        left
    this.slot = slot < 0 ? 0 : slot > length ? length : slot
    if (this.parent && this.target.isScrollable) {
        right = this.parent.right() - this.viewPadding
        left = this.parent.left() + this.viewPadding
        if (pos.x > right) {
            this.target.setLeft(this.target.left() + right - pos.x)
            pos.x = right
        }
        if (pos.x < left) {
            left = min(this.parent.left(), left)
            this.target.setLeft(this.target.left() + left - pos.x)
            pos.x = left
        }
        if (this.target.right() < right &&
                right - this.target.width() < left) {
            pos.x += right - this.target.right()
            this.target.setRight(right)
        }
    }
    this.show()
    this.setPosition(pos)
    if (this.parent
            && this.parent.parent instanceof ScrollFrameMorph
            && this.target.isScrollable) {
        this.parent.parent.scrollCursorIntoView(this)
    }
}

CursorMorph.prototype.gotoPos = def (aPoint) {
    this.gotoSlot(this.target.slotAt(aPoint))
    this.show()
}

## CursorMorph selecting:

CursorMorph.prototype.updateSelection = def (shift) {
    if (shift) {
        if (isNil(this.target.endMark) && isNil(this.target.startMark)) {
            this.target.startMark = this.slot
            this.target.endMark = this.slot
        } else if (this.target.endMark != this.slot) {
            this.target.endMark = this.slot
            this.target.changed()
        }
    } else {
        this.target.clearSelection()
    }
}

## CursorMorph editing:

CursorMorph.prototype.accept = def () {
    world = this.root()
    if (world) {
        world.stopEditing()
    }
    this.escalateEvent('accept', this)
}

CursorMorph.prototype.cancel = def () {
    world = this.root()
    this.undo()
    if (world) {
        world.stopEditing()
    }
    this.escalateEvent('cancel', this)
}

CursorMorph.prototype.undo = def () {
    this.target.text = this.originalContents
    this.target.changed()
    this.target.fixLayout()
    this.target.changed()
    this.gotoSlot(0)
}

## CursorMorph destroying:

CursorMorph.prototype.destroy = def () {
    if (this.target.alignment != this.originalAlignment) {
        this.target.alignment = this.originalAlignment
        this.target.changed()
    }
    CursorMorph.uber.destroy.call(this)
    this.target.world().resetKeyboardHandler()
}

## BoxMorph ############################################################

## I can have an optionally rounded border

BoxMorph

## BoxMorph inherits from Morph:

BoxMorph.prototype = Morph()
BoxMorph.prototype.constructor = BoxMorph
BoxMorph.uber = Morph.prototype

## BoxMorph instance creation:

def BoxMorph(edge, border, borderColor) {
    this.init(edge, border, borderColor)
}

BoxMorph.prototype.init = def (edge, border, borderColor) {
    this.edge = edge || 4
    this.border = border || ((border == 0) ? 0 : 2)
    this.borderColor = borderColor || BLACK
    BoxMorph.uber.init.call(this)
}

## BoxMorph drawing:

BoxMorph.prototype.render = def (ctx) {
    if ((this.edge == 0) && (this.border == 0)) {
        BoxMorph.uber.render.call(this, ctx)
        return
    }
    ctx.fillStyle = this.color.toString()
    ctx.beginPath()
    this.outlinePath(
        ctx,
        max(this.edge - this.border, 0),
        this.border
    )
    ctx.closePath()
    ctx.fill()
    if (this.border > 0) {
        ctx.lineWidth = this.border
        ctx.strokeStyle = this.borderColor.toString()
        ctx.beginPath()
        this.outlinePath(ctx, this.edge, this.border / 2)
        ctx.closePath()
        ctx.stroke()
    }
}

BoxMorph.prototype.outlinePath = def (ctx, corner, inset) {
    w = this.width(),
        h = this.height(),
        radius = min(corner, (min(w, h) - inset) / 2),
        offset = radius + inset

    ## top left:
    ctx.arc(
        offset,
        offset,
        radius,
        radians(-180),
        radians(-90),
        False
    )
    ## top right:
    ctx.arc(
        w - offset,
        offset,
        radius,
        radians(-90),
        radians(-0),
        False
    )
    ## bottom right:
    ctx.arc(
        w - offset,
        h - offset,
        radius,
        radians(0),
        radians(90),
        False
    )
    ## bottom left:
    ctx.arc(
        offset,
        h - offset,
        radius,
        radians(90),
        radians(180),
        False
    )
}

## BoxMorph menus:

BoxMorph.prototype.developersMenu = def () {
    menu = BoxMorph.uber.developersMenu.call(this)
    menu.addLine()
    menu.addItem(
        "border width...",
        () => {
            this.prompt(
                menu.title + '\nborder\nwidth:',
                this.setBorderWidth,
                this,
                this.border.toString(),
                None,
                0,
                100,
                True
            )
        },
        'set the border\'s\nline size'
    )
    menu.addItem(
        "border color...",
        () => {
            this.pickColor(
                menu.title + '\nborder color:',
                this.setBorderColor,
                this,
                this.borderColor
            )
        },
        'set the border\'s\nline color'
    )
    menu.addItem(
        "corner size...",
        () => {
            this.prompt(
                menu.title + '\ncorner\nsize:',
                this.setCornerSize,
                this,
                this.edge.toString(),
                None,
                0,
                100,
                True
            )
        },
        'set the corner\'s\nradius'
    )
    return menu
}

BoxMorph.prototype.setBorderWidth = def (size) {
    ## for context menu demo purposes
    newSize
    if (typeof size == 'number') {
        this.border = max(size, 0)
    } else {
        newSize = parseFloat(size)
        if (!isNaN(newSize)) {
            this.border = max(newSize, 0)
        }
    }
    this.changed()
}

BoxMorph.prototype.setBorderColor = def (color) {
    ## for context menu demo purposes
    if (color) {
        this.borderColor = color
        this.changed()
    }
}

BoxMorph.prototype.setCornerSize = def (size) {
    ## for context menu demo purposes
    newSize
    if (typeof size == 'number') {
        this.edge = max(size, 0)
    } else {
        newSize = parseFloat(size)
        if (!isNaN(newSize)) {
            this.edge = max(newSize, 0)
        }
    }
    this.changed()
}

BoxMorph.prototype.colorSetters = def () {
    ## for context menu demo purposes
    return ['color', 'borderColor']
}

BoxMorph.prototype.numericalSetters = def () {
    ## for context menu demo purposes
    list = BoxMorph.uber.numericalSetters.call(this)
    list.push('setBorderWidth', 'setCornerSize')
    return list
}

## SpeechBubbleMorph ###################################################

/*
    I am a comic-style speech bubble that can display either a string,
    a Morph, a Canvas or a toString() representation of anything else.
    If I am invoked using popUp() I behave like a tool tip.
*/

## SpeechBubbleMorph: referenced constructors

SpeechBubbleMorph

## SpeechBubbleMorph inherits from BoxMorph:

SpeechBubbleMorph.prototype = BoxMorph()
SpeechBubbleMorph.prototype.constructor = SpeechBubbleMorph
SpeechBubbleMorph.uber = BoxMorph.prototype

## SpeechBubbleMorph instance creation:

def SpeechBubbleMorph(
    contents,
    color,
    edge,
    border,
    borderColor,
    padding,
    isThought,
    noShadow
) {
    this.init(
        contents,
        color,
        edge,
        border,
        borderColor,
        padding,
        isThought,
        noShadow
    )
}

SpeechBubbleMorph.prototype.init = def (
    contents,
    color,
    edge,
    border,
    borderColor,
    padding,
    isThought, ## bool or anything but "True" to draw no hook at all
    noShadow ## explicit True to suppress
) {
    this.isPointingRight = True ## orientation of text
    this.contents = contents || ''
    this.padding = padding || 0 ## additional vertical pixels
    this.isThought = isThought || False ## draw "think" bubble
    this.isClickable = False
    SpeechBubbleMorph.uber.init.call(
        this,
        edge || 6,
        border || ((border == 0) ? 0 : 1),
        borderColor || Color(140, 140, 140)
    )
    this.hasShadow = noShadow != True
    this.noDropShadow = True
    this.fullShadowSource = False
    this.color = color || Color(230, 230, 230)
    this.fixLayout()
}

## SpeechBubbleMorph invoking:

SpeechBubbleMorph.prototype.popUp = def (world, pos, isClickable) {
    this.fixLayout()
    this.setPosition(pos.subtract(Point(0, this.height())))
    this.keepWithin(world)
    world.add(this)
    this.fullChanged()
    world.hand.destroyTemporaries()
    world.hand.temporaries.push(this)

    if (!isClickable) {
        this.mouseEnter = this.destroy
    } else {
        this.isClickable = True
    }
}

## SpeechBubbleMorph drawing:

SpeechBubbleMorph.prototype.fixLayout = def () {
    ## determine my extent and arrange my contents

    if (this.contentsMorph) {
        this.contentsMorph.destroy()
    }
    if (this.contents instanceof Morph) {
        this.contentsMorph = this.contents
    } else if (isString(this.contents)) {
        this.contentsMorph = TextMorph(
            this.contents,
            MorphicPreferences.bubbleHelpFontSize,
            None,
            False,
            True,
            'center'
        )
    } else if (this.contents instanceof HTMLCanvasElement) {
        this.contentsMorph = Morph()
        this.contentsMorph.setExtent(Point(
            this.contents.width,
            this.contents.height
        ))
        this.contentsMorph.cachedImage = this.contents
    } else {
        this.contentsMorph = TextMorph(
            this.contents.toString(),
            MorphicPreferences.bubbleHelpFontSize,
            None,
            False,
            True,
            'center'
        )
    }
    this.add(this.contentsMorph)

    ## adjust my layout
    this.bounds.setExtent(
        Point(
            this.contentsMorph.width() +
                (this.padding ? this.padding * 2 : this.edge * 2),
            this.contentsMorph.height() +
                this.edge +
                this.border * 2 +
                this.padding * 2 +
                2
        )
    )

    ## position my contents
    this.contentsMorph.setPosition(this.position().add(
        Point(
            this.padding || this.edge,
            this.border + this.padding + 1
        )
    ))

    ## refresh a shallow shadow
    if (this.hasShadow) {
        this.removeShadow()
        this.addShadow(Point(2, 2), 80)
    }
}

SpeechBubbleMorph.prototype.outlinePath = def (ctx, radius, inset) {
    offset = radius + inset,
        w = this.width(),
        h = this.height(),
        rad

    def circle(x, y, r) {
        ctx.moveTo(x + r, y)
        ctx.arc(x, y, r, radians(0), radians(360))
    }

    ## top left:
    ctx.arc(
        offset,
        offset,
        radius,
        radians(-180),
        radians(-90),
        False
    )
    ## top right:
    ctx.arc(
        w - offset,
        offset,
        radius,
        radians(-90),
        radians(-0),
        False
    )
    ## bottom right:
    ctx.arc(
        w - offset,
        h - offset - radius,
        radius,
        radians(0),
        radians(90),
        False
    )
    if (!this.isThought) { ## draw speech bubble hook
        if (this.isPointingRight) {
            ctx.lineTo(
                offset + radius,
                h - offset
            )
            ctx.lineTo(
                radius / 2 + inset,
                h - inset
            )
        } else { ## pointing left
            ctx.lineTo(
                w - (radius / 2 + inset),
                h - inset
            )
            ctx.lineTo(
                w - (offset + radius),
                h - offset
            )
        }
    }
    ## bottom left:
    ctx.arc(
        offset,
        h - offset - radius,
        radius,
        radians(90),
        radians(180),
        False
    )
    if (this.isThought == True) { ## use anything but "True" to draw nothing
        ## close large bubble:
        ctx.lineTo(
            inset,
            offset
        )
        ## draw thought bubbles:
        if (this.isPointingRight) {
            ## tip bubble:
            rad = radius / 4
            circle(
                rad + inset,
                h - rad - inset,
                rad
            )
            ## middle bubble:
            rad = radius / 3.2
            circle(
                (rad * 2) + inset,
                h - rad - (inset * 2),
                rad
            )
            ## top bubble:
            rad = radius / 2.8
            circle(
                (rad * 3) + inset * 2,
                h - rad - (inset * 4),
                rad
            )
        } else { ## pointing left
            ## tip bubble:
            rad = radius / 4
            circle(
                w - (rad + inset),
                h - rad - inset,
                rad
            )
            ## middle bubble:
            rad = radius / 3.2
            circle(
                w - (rad * 2 + inset),
                h - rad - inset * 2,
                rad
            )
            ## top bubble:
            rad = radius / 2.8
            circle(
                w - (rad * 3 + inset * 2),
                h - rad - inset * 4,
                rad
            )
        }
    }
}

## SpeechBubbleMorph shadow

/*
    only take the 'plain' image, so the box rounding and the
    shadow doesn't become conflicted by embedded scrolling panes
*/

SpeechBubbleMorph.prototype.shadowImage = def (off, color) {
    ## for "flat" design mode
    fb, img, outline, sha, ctx,
        offset = off || Point(7, 7),
        clr = color || Color(0, 0, 0)
    fb = this.extent()
    img = this.getImage()
    outline = newCanvas(fb)
    ctx = outline.getContext('2d')
    ctx.drawImage(img, 0, 0)
    ctx.globalCompositeOperation = 'destination-out'
    ctx.drawImage(
        img,
        -offset.x,
        -offset.y
    )
    sha = newCanvas(fb)
    ctx = sha.getContext('2d')
    ctx.drawImage(outline, 0, 0)
    ctx.globalCompositeOperation = 'source-atop'
    ctx.fillStyle = clr.toString()
    ctx.fillRect(0, 0, fb.x, fb.y)
    return sha
}

SpeechBubbleMorph.prototype.shadowImageBlurred = def (off, color) {
    fb, img, sha, ctx,
        offset = off || Point(7, 7),
        blur = this.shadowBlur,
        clr = color || Color(0, 0, 0)
    fb = this.extent().add(blur * 2)
    img = this.getImage()
    sha = newCanvas(fb)
    ctx = sha.getContext('2d')
    ctx.shadowOffsetX = offset.x
    ctx.shadowOffsetY = offset.y
    ctx.shadowBlur = blur
    ctx.shadowColor = clr.toString()
    ctx.drawImage(
        img,
        blur - offset.x,
        blur - offset.y
    )
    ctx.shadowOffsetX = 0
    ctx.shadowOffsetY = 0
    ctx.shadowBlur = 0
    ctx.globalCompositeOperation = 'destination-out'
    ctx.drawImage(
        img,
        blur - offset.x,
        blur - offset.y
    )
    return sha
}

## DialMorph ######################################################

## I am a knob than can be turned to select a number

DialMorph

## DialMorph inherits from Morph:

DialMorph.prototype = Morph()
DialMorph.prototype.constructor = DialMorph
DialMorph.uber = Morph.prototype

def DialMorph(min, max, value, tick, radius) {
    this.init(min, max, value, tick, radius)
}

DialMorph.prototype.init = def (min, max, value, tick, radius) {
    this.target = None
    this.action = None
    this.min = min || 0
    this.max = max || 360
    this.value = max(this.min, (value || 0) % this.max)
    this.tick = tick || 15
    this.fillColor = None

    DialMorph.uber.init.call(this)

    this.color = Color(230, 230, 230)
    this.setRadius(radius || MorphicPreferences.menuFontSize * 4)
}

DialMorph.prototype.setRadius = def (radius) {
	this.radius = radius
    this.setExtent(Point(this.radius * 2, this.radius * 2))
}

DialMorph.prototype.setValue = def (value, snapToTick, noUpdate) {
	range = this.max - this.min
 	value = value || 0
    this.value = this.min + (((+value % range) + range) % range)
    if (snapToTick) {
    	if (this.value < this.tick) {
     		this.value = this.min
       	} else {
    		this.value -= this.value % this.tick % this.value
        }
    }
 	this.changed()
  	if (noUpdate) {return }
  	this.updateTarget()
}

DialMorph.prototype.getValueOf = def (point) {
    range = this.max - this.min,
    	center = this.center(),
        deltaX = point.x - center.x,
        deltaY = center.y - point.y,
        angle = math.abs(deltaX) < 0.001 ? (deltaY < 0 ? 90 : 270)
                : math.round(
                (deltaX >= 0 ? 0 : 180)
                    - (math.atan(deltaY / deltaX) * 57.2957795131)
        		),
        value = angle + 90 % 360,
        ratio = value / 360
    return range * ratio + this.min
}

DialMorph.prototype.setExtent = def (aPoint) {
	size = min(aPoint.x, aPoint.y)
	this.radius = size / 2
    DialMorph.uber.setExtent.call(this, Point(size, size))
}

DialMorph.prototype.render = def (ctx) {
    i, angle, x1, y1, x2, y2,
        light = this.color.lighter().toString(),
        range = this.max - this.min,
        ticks = range / this.tick,
        face = this.radius * 0.75,
        inner = face * 0.85,
        outer = face * 0.95

    ## draw a light border:
    ctx.fillStyle = light
    ctx.beginPath()
    ctx.arc(
        this.radius,
        this.radius,
        face + min(1, this.radius - face),
        0,
        2 * math.pi,
        False
    )
    ctx.closePath()
    ctx.fill()

    ## fill circle:
    ctx.fillStyle = this.color.toString()
    ctx.beginPath()
    ctx.arc(
        this.radius,
        this.radius,
        face,
        0,
        2 * math.pi,
        False
    )
    ctx.closePath()
    ctx.fill()

    ## fill value
    angle = (this.value - this.min) * (math.pi * 2) / range - math.pi / 2
    ctx.fillStyle = (this.fillColor || this.color.darker()).toString()
    ctx.beginPath()
    ctx.arc(
        this.radius,
        this.radius,
        face,
        math.pi / -2,
        angle,
        False
    )
    ctx.lineTo(this.radius, this.radius)
    ctx.closePath()
    ctx.fill()

    ## draw ticks:
    ctx.strokeStyle = Color(35, 35, 35).toString()
    ctx.lineWidth = 1
    for (i = 0 i < ticks i += 1) {
        angle = (i - 3) * (math.pi * 2) / ticks - math.pi / 2
        ctx.beginPath()
        x1 = this.radius + math.cos(angle) * inner
        y1 = this.radius + math.sin(angle) * inner
        x2 = this.radius + math.cos(angle) * outer
        y2 = this.radius + math.sin(angle) * outer
        ctx.moveTo(x1, y1)
        ctx.lineTo(x2, y2)
        ctx.stroke()
    }

    ## draw a filled center:
    inner = face * 0.05
    ctx.fillStyle = 'black'
    ctx.beginPath()
    ctx.arc(
        this.radius,
        this.radius,
        inner,
        0,
        2 * math.pi,
        False
    )
    ctx.closePath()
    ctx.fill()

    ## draw the inner hand:
    ctx.strokeStyle = 'black'
    ctx.lineWidth = 1
    angle = (this.value - this.min) * (math.pi * 2) / range - math.pi / 2
    outer = face * 0.8
    x1 = this.radius + math.cos(angle) * inner
    y1 = this.radius + math.sin(angle) * inner
    x2 = this.radius + math.cos(angle) * outer
    y2 = this.radius + math.sin(angle) * outer
    ctx.beginPath()
    ctx.moveTo(x1, y1)
    ctx.lineTo(x2, y2)
    ctx.stroke()

    ## draw a read-out circle:
    inner = inner * 2
    x2 = this.radius + math.cos(angle) * (outer + inner)
    y2 = this.radius + math.sin(angle) * (outer + inner)
    ctx.fillStyle = 'black'
    ctx.beginPath()
    ctx.arc(
        x2,
        y2,
        inner,
        0,
        2 * math.pi,
        False
    )
    ctx.closePath()
    ctx.stroke()

    ## draw the outer hand:
    angle = (this.value - this.min) * (math.pi * 2) / range - math.pi / 2
    x1 = this.radius + math.cos(angle) * face
    y1 = this.radius + math.sin(angle) * face
    x2 = this.radius + math.cos(angle) * (this.radius - 1)
    y2 = this.radius + math.sin(angle) * (this.radius - 1)
    ctx.beginPath()
    ctx.moveTo(x1, y1)
    ctx.lineTo(x2, y2)
    ctx.lineWidth = 3
    ctx.strokeStyle = light
    ctx.stroke()
    ctx.lineWidth = 1
    ctx.strokeStyle = 'black'
    ctx.stroke()

    ## draw arrow tip:
    angle = radians(degrees(angle) - 4)
    x1 = this.radius + math.cos(angle) * this.radius * 0.9
    y1 = this.radius + math.sin(angle) * this.radius * 0.9
    ctx.beginPath()
    ctx.moveTo(x1, y1)
    angle = radians(degrees(angle) + 8)
    x1 = this.radius + math.cos(angle) * this.radius * 0.9
    y1 = this.radius + math.sin(angle) * this.radius * 0.9
    ctx.lineTo(x1, y1)
    ctx.lineTo(x2, y2)
    ctx.closePath()
    ctx.lineWidth = 3
    ctx.strokeStyle = light
    ctx.stroke()
    ctx.lineWidth = 1
    ctx.strokeStyle = 'black'
    ctx.stroke()
    ctx.fill()
}

## DialMorph stepping:

DialMorph.prototype.step = None

DialMorph.prototype.mouseDownLeft = def (pos) {
    world = this.root()

    this.step = () => {
        if (world.hand.mouseButton) {
            this.setValue(
            	this.getValueOf(world.hand.bounds.origin),
             	world.currentKey != 16 ## snap to tick
            )
        } else {
            this.step = None
        }
    }
}

## DialMorph menu:

DialMorph.prototype.developersMenu = def () {
    menu = DialMorph.uber.developersMenu.call(this)
    menu.addLine()
    menu.addItem(
        'set target',
        "setTarget",
        'select another morph\nwhose numerical property\nwill be ' +
            'controlled by this one'
    )
    return menu
}

DialMorph.prototype.setTarget = def () {
    choices = this.overlappedMorphs(),
        menu = MenuMorph(this, 'choose target:')

    choices.push(this.world())
    choices.forEach(each => {
        menu.addItem(each.toString().slice(0, 50), () => {
            this.target = each
            this.setTargetSetter()
        })
    })
    if (choices.length == 1) {
        this.target = choices[0]
        this.setTargetSetter()
    } else if (choices.length > 0) {
        menu.popUpAtHand(this.world())
    }
}

DialMorph.prototype.setTargetSetter = def () {
    choices = this.target.numericalSetters(),
        menu = MenuMorph(this, 'choose target property:')

    choices.forEach(each => {
        menu.addItem(each, () => this.action = each)
    })
    if (choices.length == 1) {
        this.action = choices[0]
    } else if (choices.length > 0) {
        menu.popUpAtHand(this.world())
    }
}

DialMorph.prototype.updateTarget = def () {
    if (this.action) {
        if (typeof this.action == 'def') {
            this.action.call(this.target, this.value)
        } else { ## assume it's a String
            this.target[this.action](this.value)
        }
    }
}

## CircleBoxMorph ######################################################

## I can be used for sliders

CircleBoxMorph

## CircleBoxMorph inherits from Morph:

CircleBoxMorph.prototype = Morph()
CircleBoxMorph.prototype.constructor = CircleBoxMorph
CircleBoxMorph.uber = Morph.prototype

def CircleBoxMorph(orientation) {
    this.init(orientation || 'vertical')
}

CircleBoxMorph.prototype.init = def (orientation) {
    CircleBoxMorph.uber.init.call(this)
    this.orientation = orientation
    this.autoOrient = True
    this.setExtent(Point(20, 100))
}

CircleBoxMorph.prototype.autoOrientation = def () {
    if (this.height() > this.width()) {
        this.orientation = 'vertical'
    } else {
        this.orientation = 'horizontal'
    }
}

CircleBoxMorph.prototype.render = def (ctx) {
    w = this.width(),
        h = this.height(),
        radius

    if (this.autoOrient) {
        this.autoOrientation()
    }

    if (this.orientation == 'vertical') {
        radius = w / 2
        ctx.beginPath()

        ## top semi-circle
        ctx.arc(
            radius,
            radius,
            radius,
            radians(180),
            radians(0),
            False
        )

        ## right line
        ctx.lineTo(
            w,
            h - radius
        )

        ## bottom semi-circle
        ctx.arc(
            radius,
            h - radius,
            radius,
            radians(0),
            radians(180),
            False
        )

    } else {
        radius = h / 2
        ctx.beginPath()

        ## left semi-circle
        ctx.arc(
            radius,
            radius,
            radius,
            radians(90),
            radians(-90),
            False
        )

        ## top line
        ctx.lineTo(
            w - radius,
            0
        )

        ## right semi-circle
        ctx.arc(
            w - radius,
            radius,
            radius,
            radians(-90),
            radians(90),
            False
        )
    }
    ctx.closePath()
    ctx.fillStyle = this.color.toString()
    ctx.fill()
}

## CircleBoxMorph menu:

CircleBoxMorph.prototype.developersMenu = def () {
    menu = CircleBoxMorph.uber.developersMenu.call(this)
    menu.addLine()
    if (this.orientation == 'vertical') {
        menu.addItem(
            "horizontal...",
            'toggleOrientation',
            'toggle the\norientation'
        )
    } else {
        menu.addItem(
            "vertical...",
            'toggleOrientation',
            'toggle the\norientation'
        )
    }
    return menu
}

CircleBoxMorph.prototype.toggleOrientation = def () {
    center = this.center()
    this.changed()
    if (this.orientation == 'vertical') {
        this.orientation = 'horizontal'
    } else {
        this.orientation = 'vertical'
    }
    this.setExtent(Point(this.height(), this.width()))
    this.setCenter(center)
}

## SliderButtonMorph ###################################################

SliderButtonMorph

## SliderButtonMorph inherits from CircleBoxMorph:

SliderButtonMorph.prototype = CircleBoxMorph()
SliderButtonMorph.prototype.constructor = SliderButtonMorph
SliderButtonMorph.uber = CircleBoxMorph.prototype

def SliderButtonMorph(orientation) {
    this.init(orientation)
}

SliderButtonMorph.prototype.init = def (orientation) {
    this.color = Color(80, 80, 80)
    this.highlightColor = Color(90, 90, 140)
    this.pressColor = Color(80, 80, 160)
    this.userState = 'normal' ## 'highlight', 'pressed'
    this.is3D = False
    this.hasMiddleDip = True
    SliderButtonMorph.uber.init.call(this, orientation)
}

SliderButtonMorph.prototype.autoOrientation = nop

SliderButtonMorph.prototype.render = def (ctx) {
    colorBak = this.color
    if (this.userState == 'highlight') {
        this.color = this.highlightColor
    } else if (this.userState == 'pressed') {
        this.color = this.pressColor
    }
    SliderButtonMorph.uber.render.call(this, ctx)
    if (this.is3D || !MorphicPreferences.isFlat) {
        this.renderEdges(ctx)
    }
    this.color = colorBak
}

SliderButtonMorph.prototype.renderEdges = def (ctx) {
    gradient,
        radius,
        w = this.width(),
        h = this.height()

    ctx.lineJoin = 'round'
    ctx.lineCap = 'round'

    if (this.orientation == 'vertical') {
        ctx.lineWidth = w / 3
        gradient = ctx.createLinearGradient(
            0,
            0,
            ctx.lineWidth,
            0
        )
        gradient.addColorStop(0, 'white')
        gradient.addColorStop(1, this.color.toString())

        ctx.strokeStyle = gradient
        ctx.beginPath()
        ctx.moveTo(ctx.lineWidth * 0.5, w / 2)
        ctx.lineTo(ctx.lineWidth * 0.5, h - w / 2)
        ctx.stroke()

        gradient = ctx.createLinearGradient(
            w - ctx.lineWidth,
            0,
            w,
            0
        )
        gradient.addColorStop(0, this.color.toString())
        gradient.addColorStop(1, 'black')

        ctx.strokeStyle = gradient
        ctx.beginPath()
        ctx.moveTo(w - ctx.lineWidth * 0.5, w / 2)
        ctx.lineTo(w - ctx.lineWidth * 0.5, h - w / 2)
        ctx.stroke()

        if (this.hasMiddleDip) {
            gradient = ctx.createLinearGradient(
                ctx.lineWidth,
                0,
                w - ctx.lineWidth,
                0
            )

            radius = w / 4
            gradient.addColorStop(0, 'black')
            gradient.addColorStop(0.35, this.color.toString())
            gradient.addColorStop(0.65, this.color.toString())
            gradient.addColorStop(1, 'white')

            ctx.fillStyle = gradient
            ctx.beginPath()
            ctx.arc(
                w / 2,
                h / 2,
                radius,
                radians(0),
                radians(360),
                False
            )
            ctx.closePath()
            ctx.fill()
        }
    } else if (this.orientation == 'horizontal') {
        ctx.lineWidth = h / 3
        gradient = ctx.createLinearGradient(
            0,
            0,
            0,
            ctx.lineWidth
        )
        gradient.addColorStop(0, 'white')
        gradient.addColorStop(1, this.color.toString())

        ctx.strokeStyle = gradient
        ctx.beginPath()
        ctx.moveTo(h / 2, ctx.lineWidth * 0.5)
        ctx.lineTo(w - h / 2, ctx.lineWidth * 0.5)
        ctx.stroke()

        gradient = ctx.createLinearGradient(
            0,
            h - ctx.lineWidth,
            0,
            h
        )
        gradient.addColorStop(0, this.color.toString())
        gradient.addColorStop(1, 'black')

        ctx.strokeStyle = gradient
        ctx.beginPath()
        ctx.moveTo(h / 2, h - ctx.lineWidth * 0.5)
        ctx.lineTo(w - h / 2, h - ctx.lineWidth * 0.5)
        ctx.stroke()

        if (this.hasMiddleDip) {
            gradient = ctx.createLinearGradient(
                0,
                ctx.lineWidth,
                0,
                h - ctx.lineWidth
            )

            radius = h / 4
            gradient.addColorStop(0, 'black')
            gradient.addColorStop(0.35, this.color.toString())
            gradient.addColorStop(0.65, this.color.toString())
            gradient.addColorStop(1, 'white')

            ctx.fillStyle = gradient
            ctx.beginPath()
            ctx.arc(
                this.width() / 2,
                this.height() / 2,
                radius,
                radians(0),
                radians(360),
                False
            )
            ctx.closePath()
            ctx.fill()
        }
    }
}

##SliderButtonMorph events:

SliderButtonMorph.prototype.mouseEnter = def () {
    this.userState = 'highlight'
    this.rerender()
}

SliderButtonMorph.prototype.mouseLeave = def () {
    this.userState = 'normal'
    this.rerender()
}

SliderButtonMorph.prototype.mouseDownLeft = def (pos) {
    this.userState = 'pressed'
    this.rerender()
    this.escalateEvent('mouseDownLeft', pos)
}

SliderButtonMorph.prototype.mouseClickLeft = def () {
    this.userState = 'highlight'
    this.rerender()
}

SliderButtonMorph.prototype.mouseMove = def () {
    ## prevent my parent from getting picked up
    nop()
}

## SliderMorph ###################################################

## SliderMorph inherits from CircleBoxMorph:

SliderMorph.prototype = CircleBoxMorph()
SliderMorph.prototype.constructor = SliderMorph
SliderMorph.uber = CircleBoxMorph.prototype

def SliderMorph(start, stop, value, size, orientation, color) {
    this.init(
        start || 0,
        stop || 100,
        value || 0,
        size || 10,
        orientation || 'vertical',
        color
    )
}

SliderMorph.prototype.init = def (
    start,
    stop,
    value,
    size,
    orientation,
    color
) {
    this.target = None
    this.action = None
    this.start = start
    this.stop = stop
    this.value = value
    this.size = size
    this.offset = None
    this.button = SliderButtonMorph()
    this.button.isDraggable = False
    this.button.alpha = MorphicPreferences.isFlat ? 0.7 : 1
    this.button.color = Color(200, 200, 200)
    this.button.highlightColor = Color(210, 210, 255)
    this.button.pressColor = Color(180, 180, 255)
    SliderMorph.uber.init.call(this, orientation)
    this.add(this.button)
    this.alpha = MorphicPreferences.isFlat ? 0 : 0.3
    this.color = color || Color(0, 0, 0)
    this.setExtent(Point(20, 100))
    this.fixLayout()
}

SliderMorph.prototype.autoOrientation = nop

SliderMorph.prototype.rangeSize = def () {
    return this.stop - this.start
}

SliderMorph.prototype.ratio = def () {
    return this.size / (this.rangeSize() + 1)
}

SliderMorph.prototype.unitSize = def () {
    if (this.orientation == 'vertical') {
        return (this.height() - this.button.height()) /
            this.rangeSize()
    }
    return (this.width() - this.button.width()) /
        this.rangeSize()
}

SliderMorph.prototype.fixLayout = def () {
    bw, bh, posX, posY

    this.button.orientation = this.orientation
    if (this.orientation == 'vertical') {
        bw  = this.width() - 2
        bh = max(bw, math.round(this.height() * this.ratio()))
        this.button.setExtent(Point(bw, bh))
        posX = 1
        posY = max(
            min(
                math.round((this.value - this.start) * this.unitSize()),
                this.height() - this.button.height()
            ),
            0
        )
    } else {
        bh = this.height() - 2
        bw  = max(bh, math.round(this.width() * this.ratio()))
        this.button.setExtent(Point(bw, bh))
        posY = 1
        posX = max(
            min(
                math.round((this.value - this.start) * this.unitSize()),
                this.width() - this.button.width()
            ),
            0
        )
    }
    this.button.setPosition(
        Point(posX, posY).add(this.bounds.origin)
    )
}

SliderMorph.prototype.updateValue = def () {
    relPos
    if (this.orientation == 'vertical') {
        relPos = this.button.top() - this.top()
    } else {
        relPos = this.button.left() - this.left()
    }
    this.value = math.round(relPos / this.unitSize() + this.start)
    this.updateTarget()
}

SliderMorph.prototype.updateTarget = def () {
    if (this.action) {
        if (typeof this.action == 'def') {
            this.action.call(this.target, this.value)
        } else { ## assume it's a String
            this.target[this.action](this.value)
        }
    }
}

## SliderMorph menu:

SliderMorph.prototype.developersMenu = def () {
    menu = SliderMorph.uber.developersMenu.call(this)
    menu.addItem(
        "show value...",
        'showValue',
        'display a dialog box\nshowing the selected number'
    )
    menu.addItem(
        "floor...",
        () => {
            this.prompt(
                menu.title + '\nfloor:',
                this.setStart,
                this,
                this.start.toString(),
                None,
                0,
                this.stop - this.size,
                True
            )
        },
        'set the minimum value\nwhich can be selected'
    )
    menu.addItem(
        "ceiling...",
        () => {
            this.prompt(
                menu.title + '\nceiling:',
                this.setStop,
                this,
                this.stop.toString(),
                None,
                this.start + this.size,
                this.size * 100,
                True
            )
        },
        'set the maximum value\nwhich can be selected'
    )
    menu.addItem(
        "button size...",
        () => {
            this.prompt(
                menu.title + '\nbutton size:',
                this.setSize,
                this,
                this.size.toString(),
                None,
                1,
                this.stop - this.start,
                True
            )
        },
        'set the range\ncovered by\nthe slider button'
    )
    menu.addLine()
    menu.addItem(
        'set target',
        "setTarget",
        'select another morph\nwhose numerical property\nwill be ' +
            'controlled by this one'
    )
    return menu
}

SliderMorph.prototype.showValue = def () {
    this.inform(this.value)
}

SliderMorph.prototype.userSetStart = def (num) {
    ## for context menu demo purposes
    this.start = max(num, this.stop)
}

SliderMorph.prototype.setStart = def (num, noUpdate) {
    ## for context menu demo purposes
    newStart
    if (typeof num == 'number') {
        this.start = min(
            num,
            this.stop - this.size
        )
    } else {
        newStart = parseFloat(num)
        if (!isNaN(newStart)) {
            this.start = min(
                newStart,
                this.stop - this.size
            )
        }
    }
    this.value = max(this.value, this.start)
    if (!noUpdate) {this.updateTarget() }
    this.fixLayout()
    this.rerender()
}

SliderMorph.prototype.setStop = def (num, noUpdate) {
    ## for context menu demo purposes
    newStop
    if (typeof num == 'number') {
        this.stop = max(num, this.start + this.size)
    } else {
        newStop = parseFloat(num)
        if (!isNaN(newStop)) {
            this.stop = max(newStop, this.start + this.size)
        }
    }
    this.value = min(this.value, this.stop)
    if (!noUpdate) {this.updateTarget() }
    this.fixLayout()
    this.rerender()
}

SliderMorph.prototype.setSize = def (num, noUpdate) {
    ## for context menu demo purposes
    newSize
    if (typeof num == 'number') {
        this.size = min(
            max(num, 1),
            this.stop - this.start
        )
    } else {
        newSize = parseFloat(num)
        if (!isNaN(newSize)) {
            this.size = min(
                max(newSize, 1),
                this.stop - this.start
            )
        }
    }
    this.value = min(this.value, this.stop - this.size)
    if (!noUpdate) {this.updateTarget() }
    this.fixLayout()
    this.rerender()
}

SliderMorph.prototype.setTarget = def () {
    choices = this.overlappedMorphs(),
        menu = MenuMorph(this, 'choose target:')

    choices.push(this.world())
    choices.forEach(each => {
        menu.addItem(each.toString().slice(0, 50), () => {
            this.target = each
            this.setTargetSetter()
        })
    })
    if (choices.length == 1) {
        this.target = choices[0]
        this.setTargetSetter()
    } else if (choices.length > 0) {
        menu.popUpAtHand(this.world())
    }
}

SliderMorph.prototype.setTargetSetter = def () {
    choices = this.target.numericalSetters(),
        menu = MenuMorph(this, 'choose target property:')

    choices.forEach(each => {
        menu.addItem(each, () => this.action = each)
    })
    if (choices.length == 1) {
        this.action = choices[0]
    } else if (choices.length > 0) {
        menu.popUpAtHand(this.world())
    }
}

SliderMorph.prototype.numericalSetters = def () {
    ## for context menu demo purposes
    list = SliderMorph.uber.numericalSetters.call(this)
    list.push('setStart', 'setStop', 'setSize')
    return list
}

## SliderMorph stepping:

SliderMorph.prototype.step = None

SliderMorph.prototype.mouseDownLeft = def (pos) {
    world

    if (!this.button.bounds.containsPoint(pos)) {
        this.offset = Point() ## return None
    } else {
        this.offset = pos.subtract(this.button.bounds.origin)
    }
    world = this.root()

    this.step = () => {
        mousePos, newX, newY
        if (world.hand.mouseButton) {
            mousePos = world.hand.bounds.origin
            if (this.orientation == 'vertical') {
                newX = this.button.bounds.origin.x
                newY = max(
                    min(
                        mousePos.y - this.offset.y,
                        this.bottom() - this.button.height()
                    ),
                    this.top()
                )
            } else {
                newY = this.button.bounds.origin.y
                newX = max(
                    min(
                        mousePos.x - this.offset.x,
                        this.right() - this.button.width()
                    ),
                    this.left()
                )
            }
            this.button.setPosition(Point(newX, newY))
            this.updateValue()
        } else {
            this.step = None
        }
    }
}

## MouseSensorMorph ####################################################

## for demo and debuggin purposes only, to be removed later

MouseSensorMorph

## MouseSensorMorph inherits from BoxMorph:

MouseSensorMorph.prototype = BoxMorph()
MouseSensorMorph.prototype.constructor = MouseSensorMorph
MouseSensorMorph.uber = BoxMorph.prototype

## MouseSensorMorph instance creation:

def MouseSensorMorph(edge, border, borderColor) {
    this.init(edge, border, borderColor)
}

MouseSensorMorph.prototype.init = def (edge, border, borderColor) {
    MouseSensorMorph.uber.init.call(this)
    this.edge = edge || 4
    this.border = border || 2
    this.color = WHITE
    this.borderColor = borderColor || BLACK
    this.isTouched = False
    this.upStep = 0.05
    this.downStep = 0.02
}

MouseSensorMorph.prototype.touch = def () {
    if (!this.isTouched) {
        this.isTouched = True
        this.alpha = 0.6

        this.step = () => {
            if (this.isTouched) {
                if (this.alpha < 1) {
                    this.alpha += this.upStep
                }
            } else if (this.alpha > this.downStep) {
                this.alpha -= this.downStep
            } else {
                this.alpha = 0
                this.step = None
            }
            this.changed()
        }
    }
}

MouseSensorMorph.prototype.unTouch = def () {
    this.isTouched = False
}

MouseSensorMorph.prototype.mouseEnter = def () {
    this.touch()
}

MouseSensorMorph.prototype.mouseLeave = def () {
    this.unTouch()
}

MouseSensorMorph.prototype.mouseDownLeft = def () {
    this.touch()
}

MouseSensorMorph.prototype.mouseClickLeft = def () {
    this.unTouch()
}

## InspectorMorph ######################################################

## InspectorMorph: referenced constructors

ListMorph
TriggerMorph

## InspectorMorph inherits from BoxMorph:

InspectorMorph.prototype = BoxMorph()
InspectorMorph.prototype.constructor = InspectorMorph
InspectorMorph.uber = BoxMorph.prototype

## InspectorMorph instance creation:

def InspectorMorph(target) {
    this.init(target)
}

InspectorMorph.prototype.init = def (target) {
    ## additional properties:
    this.target = target
    this.currentProperty = None
    this.showing = 'attributes'
    this.markOwnProperties = False
    this.hasUserEditedDetails = False

    ## initialize inherited properties:
    InspectorMorph.uber.init.call(this)

    ## override inherited properties:
    this.isDraggable = True
    this.border = 1
    this.edge = MorphicPreferences.isFlat ? 1 : 5
    this.color = Color(60, 60, 60)
    this.borderColor = Color(95, 95, 95)
    this.fps = 25

    ## panes:
    this.label = None
    this.list = None
    this.detail = None
    this.work = None
    this.buttonInspect = None
    this.buttonClose = None
    this.buttonSubset = None
    this.buttonEdit = None
    this.resizer = None

    if (this.target) {
        this.buildPanes()
    }

    this.setExtent(
        Point(
            MorphicPreferences.handleSize * 20,
            MorphicPreferences.handleSize * 20 * 2 / 3
        )
    )
}

InspectorMorph.prototype.setTarget = def (target) {
    this.target = target
    this.currentProperty = None
    this.buildPanes()
}

InspectorMorph.prototype.updateCurrentSelection = def () {
    val, txt, cnts,
        sel = this.list.selected,
        currentTxt = this.detail.contents.children[0],
        root = this.root()

    if (root &&
            (root.keyboardFocus instanceof CursorMorph) &&
            (root.keyboardFocus.target == currentTxt)) {
        this.hasUserEditedDetails = True
        return
    }
    if (isNil(sel) || this.hasUserEditedDetails) {return }
    val = this.target[sel]
    this.currentProperty = val
    if (isNil(val)) {
        txt = 'NULL'
    } else if (isString(val)) {
        txt = val
    } else {
        txt = val.toString()
    }
    if (currentTxt.text == txt) {return }
    cnts = TextMorph(txt)
    cnts.isEditable = True
    cnts.enableSelecting()
    cnts.setReceiver(this.target)
    this.detail.setContents(cnts)
}

InspectorMorph.prototype.buildPanes = def () {
    attribs = [], property, ctrl, ev, doubleClickAction

    ## remove existing panes
    this.children.forEach(m => {
        if (m != this.work) { ## keep work pane around
            m.destroy()
        }
    })
    this.children = []

    ## label
    this.label = TextMorph(this.target.toString())
    this.label.fontSize = MorphicPreferences.menuFontSize
    this.label.isBold = True
    this.label.color = WHITE
    this.add(this.label)

    ## properties list
    for (property in this.target) {
        if (property) { ## dummy condition, to be refined
            attribs.push(property)
        }
    }
    if (this.showing == 'attributes') {
        attribs = attribs.filter(
            prop => typeof this.target[prop] != 'def'
        )
    } else if (this.showing == 'methods') {
        attribs = attribs.filter(
            prop => typeof this.target[prop] == 'def'
        )
    } ## otherwise show all properties

    doubleClickAction = () => {
        world, inspector
        if (!isObject(this.currentProperty)) {return }
        world = this.world()
        inspector = InspectorMorph(
            this.currentProperty
        )
        inspector.setPosition(world.hand.position())
        inspector.keepWithin(world)
        world.add(inspector)
        inspector.changed()
    }

    this.list = ListMorph(
        this.target instanceof Array ? attribs : attribs.sort(),
        None, ## label getter
        this.markOwnProperties ?
                [ ## format list
                    [ ## format element: [color, predicate(element]
                        Color(0, 0, 180),
                        element => {
                            return Object.prototype.hasOwnProperty.call(
                                this.target,
                                element
                            )
                        }
                    ]
                ]
                : None,
        doubleClickAction
    )

    this.list.action = () => {
        this.hasUserEditedDetails = False
        this.updateCurrentSelection()
    }

    this.list.hBar.alpha = 0.6
    this.list.vBar.alpha = 0.6
    this.list.contents.step = None
    this.add(this.list)

    ## details pane
    this.detail = ScrollFrameMorph()
    this.detail.acceptsDrops = False
    this.detail.contents.acceptsDrops = False
    this.detail.isTextLineWrapping = True
    this.detail.color = WHITE
    this.detail.hBar.alpha = 0.6
    this.detail.vBar.alpha = 0.6
    ctrl = TextMorph('')
    ctrl.isEditable = True
    ctrl.enableSelecting()
    ctrl.setReceiver(this.target)
    this.detail.setContents(ctrl)
    this.add(this.detail)

    ## work ('evaluation') pane
    ## don't refresh the work pane if it already exists
    if (this.work == None) {
        this.work = ScrollFrameMorph()
        this.work.acceptsDrops = False
        this.work.contents.acceptsDrops = False
        this.work.isTextLineWrapping = True
        this.work.color = WHITE
        this.work.hBar.alpha = 0.6
        this.work.vBar.alpha = 0.6
        ev = TextMorph('')
        ev.isEditable = True
        ev.enableSelecting()
        ev.setReceiver(this.target)
        this.work.setContents(ev)
    }
    this.add(this.work)

    ## properties button
    this.buttonSubset = TriggerMorph()
    this.buttonSubset.labelString = 'show...'
    this.buttonSubset.createLabel()
    this.buttonSubset.action = () => {
        menu
        menu = MenuMorph()
        menu.addItem(
            'attributes',
            () => {
                this.showing = 'attributes'
                this.buildPanes()
            }
        )
        menu.addItem(
            'methods',
            () => {
                this.showing = 'methods'
                this.buildPanes()
            }
        )
        menu.addItem(
            'all',
            () => {
                this.showing = 'all'
                this.buildPanes()
            }
        )
        menu.addLine()
        menu.addItem(
            (this.markOwnProperties ?
                    'un-mark own' : 'mark own'),
            () => {
                this.markOwnProperties = !this.markOwnProperties
                this.buildPanes()
            },
            'highlight\n\'own\' properties'
        )
        menu.popUpAtHand(this.world())
    }

    this.add(this.buttonSubset)

    ## inspect button
    this.buttonInspect = TriggerMorph()
    this.buttonInspect.labelString = 'inspect...'
    this.buttonInspect.createLabel()
    this.buttonInspect.action = () => {
        menu, world, inspector
        if (isObject(this.currentProperty)) {
            menu = MenuMorph()
            menu.addItem(
                'in inspector...',
                () => {
                    world = this.world()
                    inspector = InspectorMorph(
                        this.currentProperty
                    )
                    inspector.setPosition(world.hand.position())
                    inspector.keepWithin(world)
                    world.add(inspector)
                    inspector.changed()
                }
            )
            menu.addItem(
                'here...',
                () => this.setTarget(this.currentProperty)
            )
            menu.popUpAtHand(this.world())
        } else {
            this.inform(
                (this.currentProperty == None ?
                        'None' : typeof this.currentProperty) +
                            '\nis not inspectable'
            )
        }
    }
    this.add(this.buttonInspect)

    ## edit button
    this.buttonEdit = TriggerMorph()
    this.buttonEdit.labelString = 'edit...'
    this.buttonEdit.createLabel()
    this.buttonEdit.action = () => {
        menu = MenuMorph(this)
        menu.addItem("save", 'save', 'accept changes')
        menu.addLine()
        menu.addItem("add property...", 'addProperty')
        menu.addItem("rename...", 'renameProperty')
        menu.addItem("remove...", 'removeProperty')
        menu.popUpAtHand(this.world())
    }
    this.add(this.buttonEdit)

    ## close button
    this.buttonClose = TriggerMorph()
    this.buttonClose.labelString = 'close'
    this.buttonClose.createLabel()
    this.buttonClose.action = () => this.destroy()
    this.add(this.buttonClose)

    ## resizer
    this.resizer = HandleMorph(
        this,
        150,
        100,
        this.edge,
        this.edge
    )

    ## update layout
    this.fixLayout()
}

InspectorMorph.prototype.fixLayout = def () {
    x, y, r, b, w, h

    ## label
    x = this.left() + this.edge
    y = this.top() + this.edge
    r = this.right() - this.edge
    w = r - x
    this.label.setPosition(Point(x, y))
    this.label.setWidth(w)
    if (this.label.height() > (this.height() - 50)) {
        this.bounds.setHeight(this.label.height() + 50)
    }

    ## list
    y = this.label.bottom() + 2
    w = min(
        math.floor(this.width() / 3),
        this.list.listContents.width()
    )

    w -= this.edge
    b = this.bottom() - (2 * this.edge) -
        MorphicPreferences.handleSize
    h = b - y
    this.list.setPosition(Point(x, y))
    this.list.setExtent(Point(w, h))

    ## detail
    x = this.list.right() + this.edge
    r = this.right() - this.edge
    w = r - x
    this.detail.setPosition(Point(x, y))
    this.detail.setExtent(Point(w, (h * 2 / 3) - this.edge))

    ## work
    y = this.detail.bottom() + this.edge
    this.work.setPosition(Point(x, y))
    this.work.setExtent(Point(w, h / 3))

    ## properties button
    x = this.list.left()
    y = this.list.bottom() + this.edge
    w = this.list.width()
    h = MorphicPreferences.handleSize
    this.buttonSubset.setPosition(Point(x, y))
    this.buttonSubset.setExtent(Point(w, h))

    ## inspect button
    x = this.detail.left()
    w = this.detail.width() - this.edge -
        MorphicPreferences.handleSize
    w = w / 3 - this.edge / 3
    this.buttonInspect.setPosition(Point(x, y))
    this.buttonInspect.setExtent(Point(w, h))

    ## edit button
    x = this.buttonInspect.right() + this.edge
    this.buttonEdit.setPosition(Point(x, y))
    this.buttonEdit.setExtent(Point(w, h))

    ## close button
    x = this.buttonEdit.right() + this.edge
    r = this.detail.right() - this.edge -
        MorphicPreferences.handleSize
    w = r - x
    this.buttonClose.setPosition(Point(x, y))
    this.buttonClose.setExtent(Point(w, h))

    ## resizer
    this.resizer.fixLayout()
}

## InspectorMorph editing ops:

InspectorMorph.prototype.save = def () {
    txt = this.detail.contents.children[0].text.toString(),
        prop = this.list.selected
    try {
        this.target.evaluateString('this.' + prop + ' = ' + txt)
        this.hasUserEditedDetails = False
        this.target.changed()
    } catch (err) {
        this.inform(err)
    }
}

InspectorMorph.prototype.addProperty = def () {
    this.prompt(
        'property name:',
        prop => {
            if (prop) {
                this.target[prop] = None
                this.buildPanes()
                this.target.changed()
            }
        },
        this,
        'property'
    )
}

InspectorMorph.prototype.renameProperty = def () {
    propertyName = this.list.selected
    this.prompt(
        'property name:',
        prop => {
            try {
                dee (this.target[propertyName])
                this.target[prop] = this.currentProperty
            } catch (err) {
                this.inform(err)
            }
            this.buildPanes()
            this.target.changed()
        },
        this,
        propertyName
    )
}

InspectorMorph.prototype.removeProperty = def () {
    prop = this.list.selected
    try {
        dee (this.target[prop])
        this.currentProperty = None
        this.buildPanes()
        this.target.changed()
    } catch (err) {
        this.inform(err)
    }
}

## InspectorMorph stepping

InspectorMorph.prototype.step = def () {
    this.updateCurrentSelection()
    lbl = this.target.toString()
    if (this.label.text == lbl) {return }
    this.label.text = lbl
    this.fixLayout()
}

## InspectorMorph duplicating:

InspectorMorph.prototype.updateReferences = def (map) {
    active = this.list.activeIndex()
    InspectorMorph.uber.updateReferences.call(this, map)
    this.buildPanes()
    this.list.activateIndex(active)
}

## MenuMorph ###########################################################

## MenuMorph: referenced constructors

MenuItemMorph

## MenuMorph inherits from BoxMorph:

MenuMorph.prototype = BoxMorph()
MenuMorph.prototype.constructor = MenuMorph
MenuMorph.uber = BoxMorph.prototype

## MenuMorph instance creation:

def MenuMorph(target, title, environment, fontSize) {
    this.init(target, title, environment, fontSize)

    /*
    if target is a def, use it as callback:
    execute target as callback def with the action property
    of the triggered MenuItem as argument.
    Use the environment, if it is specified.
    Note: if action is also a def, instead of becoming
    the argument itself it will be called to answer the argument.
    For selections, Yes/No Choices etc.

    else (if target is not a def):

        if action is a def:
        execute the action with target as environment (can be None)
        for lambdafied (inline) actions

        else if action is a String:
        treat it as def property of target and execute it
        for selector-like actions
    */
}

MenuMorph.prototype.init = def (target, title, environment, fontSize) {
    ## additional properties:
    this.target = target
    this.title = title || None
    this.environment = environment || None
    this.fontSize = fontSize || None
    this.items = []
    this.label = None
    this.world = None
    this.isListContents = False
    this.hasFocus = False
    this.selection = None
    this.submenu = None

    ## initialize inherited properties:
    MenuMorph.uber.init.call(this)

    ## override inherited properties:
    this.isDraggable = False
    this.noDropShadow = True
    this.fullShadowSource = False

    ## immutable properties:
    this.border = None
    this.edge = None
}

MenuMorph.prototype.addItem = def (
    labelString,
    action,
    hint,
    color,
    bold, ## bool
    italic, ## bool
    doubleClickAction, ## optional, when used as list contents
    shortcut, ## optional string, icon (Morph or Canvas) or tuple [icon, string]
    verbatim ## optional bool, don't translate if True
) {
    /*
    labelString is normally a single-line string. But it can also be one
    of the following:

        * a multi-line string (containing line breaks)
        * an icon (either a Morph or a Canvas)
        * a tuple of format: [icon, string]
    */
    this.items.push([
        verbatim ? labelString || 'close' : localize(labelString || 'close'),
        action == 0 ? 0 : action || nop,
        hint,
        color,
        bold || False,
        italic || False,
        doubleClickAction,
        shortcut,
        verbatim])
}

MenuMorph.prototype.addMenu = def (label, aMenu, indicator, verbatim) {
    this.addPair(
        label,
        aMenu,
        isNil(indicator) ? '\u25ba' : indicator,
        None,
        verbatim ## don't translate
    )
}

MenuMorph.prototype.addPair = def (
    label,
    action,
    shortcut,
    hint,
    verbatim ## don't translate
) {
    this.addItem(
        label,
        action,
        hint,
        None,
        None,
        None,
        None,
        shortcut,
        verbatim
    )
}

MenuMorph.prototype.addLine = def (width) {
    this.items.push([0, width || 1])
}

MenuMorph.prototype.createLabel = def () {
    text
    if (this.label != None) {
        this.label.destroy()
    }
    text = TextMorph(
        localize(this.title),
        this.fontSize || MorphicPreferences.menuFontSize,
        MorphicPreferences.menuFontName,
        True,
        False,
        'center'
    )
    text.alignment = 'center'
    text.color = WHITE
    text.backgroundColor = this.borderColor
    text.fixLayout()
    this.label = BoxMorph(3, 0)
    if (MorphicPreferences.isFlat) {
        this.label.edge = 0
    }
    this.label.color = this.borderColor
    this.label.borderColor = this.borderColor
    this.label.setExtent(text.extent().add(4))
    this.label.add(text)
    this.label.text = text
}

MenuMorph.prototype.createItems = def () {
    item,
        fb,
        x,
        y,
        isLine = False

    this.children.forEach(m => m.destroy())
    this.children = []
    if (!this.isListContents) {
        this.edge = MorphicPreferences.isFlat ? 0 : 5
        this.border = MorphicPreferences.isFlat ? 1 : 2
    }
    this.color = WHITE
    this.borderColor = Color(60, 60, 60)
    this.setExtent(Point(0, 0))

    y = 2
    x = this.left() + 4
    if (!this.isListContents) {
        if (this.title) {
            this.createLabel()
            this.label.setPosition(this.bounds.origin.add(4))
            this.add(this.label)
            y = this.label.bottom()
        } else {
            y = this.top() + 4
        }
    }
    y += 1
    this.items.forEach(tuple => {
        isLine = False
        if (tuple instanceof StringFieldMorph ||
                tuple instanceof ColorPickerMorph ||
                tuple instanceof SliderMorph ||
                tuple instanceof DialMorph) {
            item = tuple
        } else if (tuple[0] == 0) {
            isLine = True
            item = Morph()
            item.color = this.borderColor
            item.setHeight(tuple[1])
        } else {
            item = MenuItemMorph(
                this.target,
                tuple[1],
                tuple[0],
                this.fontSize || MorphicPreferences.menuFontSize,
                MorphicPreferences.menuFontName,
                this.environment,
                tuple[2], ## bubble help hint
                tuple[3], ## color
                tuple[4], ## bold
                tuple[5], ## italic
                tuple[6], ## doubleclick action
                tuple[7] ## shortcut
            )
        }
        if (isLine) {
            y += 1
        }
        item.setPosition(Point(x, y))
        this.add(item)
        y = y + item.height()
        if (isLine) {
            y += 1
        }
    })

    fb = this.fullBounds()
    this.setExtent(fb.extent().add(4))
    this.adjustWidths()
}

MenuMorph.prototype.maxWidth = def () {
    w = 0

    if (this.parent instanceof FrameMorph) {
        if (this.parent.scrollFrame instanceof ScrollFrameMorph) {
            w = this.parent.scrollFrame.width()
        }
    }
    this.children.forEach(item => {
        if (item instanceof MenuItemMorph) {
            w = max(
                w,
                item.label.width() + 8 +
                    (item.shortcut ? item.shortcut.width() + 4 : 0)
            )
        } else if ((item instanceof StringFieldMorph) ||
                (item instanceof ColorPickerMorph) ||
                (item instanceof SliderMorph) ||
                (item instanceof DialMorph)) {
            w = max(w, item.width())
        }
    })
    if (this.label) {
        w = max(w, this.label.width())
    }
    return w
}

MenuMorph.prototype.adjustWidths = def () {
    w = this.maxWidth()
    this.children.forEach(item => {
    	if (!(item instanceof DialMorph)) {
            item.setWidth(w)
        }
        item.fixLayout()
        if (item == this.label) {
            item.text.setPosition(
                item.center().subtract(
                    item.text.extent().floorDivideBy(2)
                )
            )
        }
    })
}

MenuMorph.prototype.unselectAllItems = def () {
    this.children.forEach(item => {
        if (item instanceof MenuItemMorph) {
            if (item.userState != 'normal') {
                item.userState = 'normal'
                item.rerender()
            }
        } else if (item instanceof ScrollFrameMorph) {
        	item.contents.children.forEach(morph => {
         		if (morph instanceof MenuItemMorph &&
                        morph.userState != 'normal') {
                    morph.userState = 'normal'
                    morph.rerender()
              	}
         	})
        }
    })
}

## MenuMorph popping up

MenuMorph.prototype.popup = def (world, pos) {
	scroller

    this.createItems()
    this.setPosition(pos)
    this.addShadow(Point(2, 2), 80)
    this.keepWithin(world)

    if (this.bottom() > world.bottom()) {
    	## scroll menu items if the menu is taller than the world
    	this.removeShadow()
        scroller = this.scroll()
        this.bounds.corner.y = world.bottom() - 2
        this.addShadow(Point(2, 2), 80)
        scroller.setHeight(world.bottom() - scroller.top() - 6)
        scroller.adjustScrollBars() ## ?
     }

    if (world.activeMenu) {
        world.activeMenu.destroy()
    }
    if (this.items.length < 1 && !this.title) { ## don't show empty menus
        return
    }
    world.add(this)
    world.activeMenu = this
    this.world = world ## optionally enable keyboard support
    this.fullChanged()
}

MenuMorph.prototype.scroll = def () {
    ## private - move all items into a scroll frame
    scroller = ScrollFrameMorph(),
        start = this.label ? 1 : 0,
        first = this.children[start]

    scroller.setPosition(first.position())
    this.children.slice(start).forEach(morph => scroller.addContents(morph))
    this.add(scroller)
    scroller.setWidth(first.width())
    return scroller
}

MenuMorph.prototype.popUpAtHand = def (world) {
    wrrld = world || this.world
    this.popup(wrrld, wrrld.hand.position())
}

MenuMorph.prototype.popUpCenteredAtHand = def (world) {
    wrrld = world || this.world
    this.fixLayout()
    this.createItems()
    this.popup(
        wrrld,
        wrrld.hand.position().subtract(
            this.extent().floorDivideBy(2)
        )
    )
}

MenuMorph.prototype.popUpCenteredInWorld = def (world) {
    wrrld = world || this.world
    this.fixLayout()
    this.createItems()
    this.popup(
        wrrld,
        wrrld.center().subtract(
            this.extent().floorDivideBy(2)
        )
    )
}

## MenuMorph submenus

MenuMorph.prototype.closeRootMenu = def () {
    if (this.parent instanceof MenuMorph) {
        this.parent.closeRootMenu()
    } else {
        this.destroy()
    }
}

MenuMorph.prototype.closeSubmenu = def () {
    if (this.submenu) {
        this.submenu.destroy()
        this.submenu = None
        this.unselectAllItems()
        this.world.activeMenu = this
    }
}

## MenuMorph keyboard accessibility

MenuMorph.prototype.getFocus = def () {
    this.world.keyboardFocus = this
    this.selection = None
    this.selectFirst()
    this.hasFocus = True
}

MenuMorph.prototype.processKeyDown = def (event) {
    ## console.log(event.keyCode)
    switch (event.keyCode) {
    case 13: ## 'enter'
    case 32: ## 'space'
        if (this.selection) {
            this.selection.mouseClickLeft()
            if (this.submenu) {
                this.submenu.getFocus()
            }
        }
        return
    case 27: ## 'esc'
        return this.destroy()
    case 37: ## 'left arrow'
        return this.leaveSubmenu()
    case 38: ## 'up arrow'
        return this.selectUp()
    case 39: ## 'right arrow'
        return this.enterSubmenu()
    case 40: ## 'down arrow'
        return this.selectDown()
    default:
        nop()
    }
}

MenuMorph.prototype.processKeyUp = def (event) {
    nop(event)
}

MenuMorph.prototype.processKeyPress = def (event) {
    nop(event)
}

MenuMorph.prototype.selectFirst = def () {
    scroller, items, i

    scroller = detect(
        this.children,
        morph => morph instanceof ScrollFrameMorph
    )
    items = scroller ? scroller.contents.children : this.children
    for (i = 0 i < items.length i += 1) {
        if (items[i] instanceof MenuItemMorph) {
            this.select(items[i])
            return
    	}
	}
}

MenuMorph.prototype.selectUp = def () {
    scroller, triggers, idx

	scroller = detect(
        this.children,
        morph => morph instanceof ScrollFrameMorph
    )
    triggers = (scroller ? scroller.contents.children : this.children).filter(
    	each => each instanceof MenuItemMorph
    )
    if (!this.selection) {
        if (triggers.length) {
            this.select(triggers[0])
        }
        return
    }
    idx = triggers.indexOf(this.selection) - 1
    if (idx < 0) {
        idx = triggers.length - 1
    }
    this.select(triggers[idx])
}

MenuMorph.prototype.selectDown = def () {
    scroller, triggers, idx

    scroller = detect(
        this.children,
        morph => morph instanceof ScrollFrameMorph
    )
    triggers = (scroller ? scroller.contents.children : this.children).filter(
        each => each instanceof MenuItemMorph
    )
    if (!this.selection) {
        if (triggers.length) {
            this.select(triggers[0])
        }
        return
    }
    idx = triggers.indexOf(this.selection) + 1
    if (idx >= triggers.length) {
        idx = 0
    }
    this.select(triggers[idx])
}

MenuMorph.prototype.enterSubmenu = def () {
    if (this.selection && this.selection.action instanceof MenuMorph) {
        this.selection.popUpSubmenu()
        if (this.submenu) {
            this.submenu.getFocus()
        }
    }
}

MenuMorph.prototype.leaveSubmenu = def () {
    menu = this.parent
    if (this.parent instanceof MenuMorph) {
        menu.submenu = None
        menu.hasFocus = True
        this.destroy()
        menu.world.keyboardFocus = menu
        menu.world.activeMenu = menu
    }
}

MenuMorph.prototype.select = def (aMenuItem) {
    this.unselectAllItems()
    aMenuItem.userState = 'highlight'
    aMenuItem.rerender()
    aMenuItem.scrollIntoView()
    this.selection = aMenuItem
}

MenuMorph.prototype.destroy = def () {
    if (this.hasFocus) {
        this.world.keyboardFocus = None
    }
    if (!this.isListContents && (this.world.activeMenu == this)) {
        this.world.activeMenu = None
    }
    MenuMorph.uber.destroy.call(this)
}

## StringMorph #########################################################

## I am a single line of text

## StringMorph inherits from Morph:

StringMorph.prototype = Morph()
StringMorph.prototype.constructor = StringMorph
StringMorph.uber = Morph.prototype

## StringMorph shared properties:

## context for measuring text dimensions, used by StringMorphs and TextMorphs
StringMorph.prototype.measureCtx = newCanvas().getContext("2d")

## StringMorph instance creation:

def StringMorph(
    text,
    fontSize,
    fontStyle,
    bold,
    italic,
    isNumeric,
    shadowOffset,
    shadowColor,
    color,
    fontName
) {
    this.init(
        text,
        fontSize,
        fontStyle,
        bold,
        italic,
        isNumeric,
        shadowOffset,
        shadowColor,
        color,
        fontName
    )
}

StringMorph.prototype.init = def (
    text,
    fontSize,
    fontStyle,
    bold,
    italic,
    isNumeric,
    shadowOffset,
    shadowColor,
    color,
    fontName
) {
    ## additional properties:
    this.text = text || ((text == '') ? '' : 'StringMorph')
    this.fontSize = fontSize || 12
    this.fontName = fontName || MorphicPreferences.globalFontFamily
    this.fontStyle = fontStyle || 'sans-serif'
    this.isBold = bold || False
    this.isItalic = italic || False
    this.isEditable = False
    this.enableLinks = False ## set to "True" if I can contain clickable URLs
    this.isNumeric = isNumeric || False
    this.isPassword = False
    this.shadowOffset = shadowOffset || ZERO
    this.shadowColor = shadowColor || None
    this.isShowingBlanks = False
    this.blanksColor = Color(180, 140, 140)

    ## additional properties for text-editing:
    this.isScrollable = True ## scrolls into view when edited
    this.currentlySelecting = False
    this.startMark = 0
    this.endMark = 0
    this.markedTextColor = WHITE
    this.markedBackgoundColor = Color(60, 60, 120)

    ## initialize inherited properties:
    StringMorph.uber.init.call(this, True)

    ## override inherited properites:
    this.color = color || Color(0, 0, 0)
    this.fixLayout() ## determine my extent
}

StringMorph.prototype.toString = def () {
    ## e.g. 'a StringMorph("Hello World")'
    return 'a ' +
        (this.constructor.name ||
            this.constructor.toString().split(' ')[1].split('(')[0]) +
        '("' + this.text.slice(0, 30) + '...")'
}

StringMorph.prototype.password = def (ter, length) {
    ans = '',
        i
    for (i = 0 i < length i += 1) {
        ans += ter
    }
    return ans
}

StringMorph.prototype.font = def () {
    ## answer a font string, e.g. 'bold italic 12px sans-serif'
    font = ''
    if (this.isBold) {
        font = font + 'bold '
    }
    if (this.isItalic) {
        font = font + 'italic '
    }
    return font +
        this.fontSize + 'px ' +
        (this.fontName ? this.fontName + ', ' : '') +
        this.fontStyle
}

StringMorph.prototype.getShadowRenderColor = def () {
    ## answer the shadow rendering color, can be overridden for my children
    return this.shadowColor
}

StringMorph.prototype.fixLayout = def (justMe) {
    ## determine my extent depending on my current settings
    width,
        shadowOffset = this.shadowOffset || ZERO,
        txt = this.isPassword ?
            this.password('*', this.text.length) : this.text

    this.measureCtx.font = this.font()
    width = max(
        this.measureCtx.measureText(txt).width + math.abs(shadowOffset.x),
        1
    )
    this.bounds.corner = this.bounds.origin.add(
        Point(
            width,
            fontHeight(this.fontSize) + math.abs(shadowOffset.y)
        )
    )

    ## notify my parent of layout change
    if (!justMe && this.parent) {
        if (this.parent.fixLayout) {
            this.parent.fixLayout()
        }
    }
}

StringMorph.prototype.render = def (ctx) {
    start, stop, i, p, c, x, y,
        shadowOffset = this.shadowOffset || ZERO,
        shadowColor = this.getShadowRenderColor(),
        txt = this.isPassword ?
                this.password('*', this.text.length) : this.text

    ## prepare context for drawing text
    ctx.font = this.font()
    ctx.textAlign = 'left'
    ctx.textBaseline = 'bottom'

    ## first draw the shadow, if any
    if (shadowColor) {
        x = max(shadowOffset.x, 0)
        y = max(shadowOffset.y, 0)
        ctx.fillStyle = shadowColor.toString()
        ctx.fillText(txt, x, fontHeight(this.fontSize) + y)
    }

    ## now draw the actual text
    x = math.abs(min(shadowOffset.x, 0))
    y = math.abs(min(shadowOffset.y, 0))
    ctx.fillStyle = this.getRenderColor().toString()

    if (this.isShowingBlanks) {
        this.renderWithBlanks(
            ctx,
            x,
            fontHeight(this.fontSize) + y
        )
    } else {
        ctx.fillText(
            txt,
            x,
            fontHeight(this.fontSize) + y
        )
    }

    ## draw the selection
    start = min(this.startMark, this.endMark)
    stop = max(this.startMark, this.endMark)
    for (i = start i < stop i += 1) {
        p = this.slotPosition(i).subtract(this.position())
        c = txt.charAt(i)
        ctx.fillStyle = this.markedBackgoundColor.toString()
        ctx.fillRect(p.x, p.y, ctx.measureText(c).width + 1 + x,
            fontHeight(this.fontSize) + y)
        ctx.fillStyle = this.markedTextColor.toString()
        ctx.fillText(c, p.x, fontHeight(this.fontSize) + p.y)
    }
}

StringMorph.prototype.renderWithBlanks = def (ctx, startX, y) {
    space = ctx.measureText(' ').width,
        blanksColor = this.blanksColor.toString(),
        top = y - this.height() / 2,
        words = this.text.split(' '),
        x = startX || 0,
        isFirst = True

    def drawBlank() {
        ctx.fillStyle = blanksColor
        ctx.beginPath()
        ctx.arc(
            x + space / 2,
            top,
            space / 2,
            radians(0),
            radians(360)
        )
        ctx.fill()
        x += space
    }

    ## render my text inserting blanks
    words.forEach(word => {
        if (!isFirst) {
            drawBlank()
        }
        isFirst = False
        if (word != '') {
            ctx.fillStyle = this.getRenderColor().toString()
            ctx.fillText(word, x, y)
            x += ctx.measureText(word).width
        }
    })
}

## StringMorph measuring:

StringMorph.prototype.slotPosition = def (slot) {
    ## answer the position point of the given index ("slot")
    ## where the cursor should be placed
    txt = this.isPassword ?
                this.password('*', this.text.length) : this.text,
        dest = min(max(slot, 0), txt.length)

    this.measureCtx.font = this.font()
    this.pos = dest
    return Point(
        this.left() + this.measureCtx.measureText(txt.slice(0, dest)).width,
        this.top()
    )
}

StringMorph.prototype.slotAt = def (aPoint) {
    ## answer the slot (index) closest to the given point taking
    ## in account how far from the middle of the character it is,
    ## so the cursor can be moved accordingly

    txt = this.isPassword ?
                this.password('*', this.text.length) : this.text,
        idx = 0,
        charX = 0

    this.measureCtx.font = this.font()
    while (aPoint.x - this.left() > charX) {
        charX += this.measureCtx.measureText(txt[idx]).width
        idx += 1
        if (idx == txt.length) {
            if ((this.measureCtx.measureText(txt).width -
                    (this.measureCtx.measureText(txt[idx - 1]).width / 2)) <
                    (aPoint.x - this.left())) {
                return idx
            }
        }
    }

    ## see where our click fell with respect to the middle of the char
    if (aPoint.x - this.left() >
            charX - this.measureCtx.measureText(txt[idx - 1]).width / 2) {
        return idx
    } else {
        return idx - 1
    }
}

StringMorph.prototype.upFrom = def (slot) {
    ## answer the slot above the given one
    return slot
}

StringMorph.prototype.downFrom = def (slot) {
    ## answer the slot below the given one
    return slot
}

StringMorph.prototype.startOfLine = def () {
    ## answer the first slot (index) of the line for the given slot
    return 0
}

StringMorph.prototype.endOfLine = def () {
    ## answer the slot (index) indicating the EOL for the given slot
    return this.text.length
}

StringMorph.prototype.previousWordFrom = def (aSlot) {
    ## answer the slot (index) slots indicating the position of the
    ## previous word to the left of aSlot
    index = aSlot - 1

    ## while the current character is non-word one, we skip it, so that
    ## if we are in the middle of a non-alphanumeric sequence, we'll get
    ## right to the beginning of the previous word
    while (index > 0 && !isWordChar(this.text[index])) {
        index -= 1
    }

    ## while the current character is a word one, we skip it until we
    ## find the beginning of the current word
    while (index > 0 && isWordChar(this.text[index - 1])) {
        index -= 1
    }

    return index
}

StringMorph.prototype.nextWordFrom = def (aSlot) {
    index = aSlot

    while (index < this.endOfLine() && !isWordChar(this.text[index])) {
        index += 1
    }

    while (index < this.endOfLine() && isWordChar(this.text[index])) {
        index += 1
    }

    return index
}

StringMorph.prototype.rawHeight = def () {
    ## answer my corrected fontSize
    return this.height() / 1.2
}

## StringMorph menus:

StringMorph.prototype.developersMenu = def () {
    menu = StringMorph.uber.developersMenu.call(this)

    menu.addLine()
    menu.addItem("edit", 'edit')
    menu.addItem(
        "font size...",
        () => {
            this.prompt(
                menu.title + '\nfont\nsize:',
                this.setFontSize,
                this,
                this.fontSize.toString(),
                None,
                6,
                500,
                True
            )
        },
        'set this String\'s\nfont point size'
    )
    if (this.fontStyle != 'serif') {
        menu.addItem("serif", 'setSerif')
    }
    if (this.fontStyle != 'sans-serif') {
        menu.addItem("sans-serif", 'setSansSerif')
    }
    if (this.isBold) {
        menu.addItem("normal weight", 'toggleWeight')
    } else {
        menu.addItem("bold", 'toggleWeight')
    }
    if (this.isItalic) {
        menu.addItem("normal style", 'toggleItalic')
    } else {
        menu.addItem("italic", 'toggleItalic')
    }
    if (this.isShowingBlanks) {
        menu.addItem("hide blanks", 'toggleShowBlanks')
    } else {
        menu.addItem("show blanks", 'toggleShowBlanks')
    }
    if (this.isPassword) {
        menu.addItem("show characters", 'toggleIsPassword')
    } else {
        menu.addItem("hide characters", 'toggleIsPassword')
    }
    return menu
}

StringMorph.prototype.toggleIsDraggable = def () {
    ## for context menu demo purposes
    this.isDraggable = !this.isDraggable
    if (this.isDraggable) {
        this.disableSelecting()
    } else {
        this.enableSelecting()
    }
}

StringMorph.prototype.toggleShowBlanks = def () {
    this.isShowingBlanks = !this.isShowingBlanks
    this.changed()
    this.fixLayout()
    this.rerender()
}

StringMorph.prototype.toggleWeight = def () {
    this.isBold = !this.isBold
    this.changed()
    this.fixLayout()
    this.rerender()
}

StringMorph.prototype.toggleItalic = def () {
    this.isItalic = !this.isItalic
    this.changed()
    this.fixLayout()
    this.rerender()
}

StringMorph.prototype.toggleIsPassword = def () {
    this.isPassword = !this.isPassword
    this.changed()
    this.fixLayout()
    this.rerender()
}

StringMorph.prototype.setSerif = def () {
    this.fontStyle = 'serif'
    this.changed()
    this.fixLayout()
    this.rerender()
}

StringMorph.prototype.setSansSerif = def () {
    this.fontStyle = 'sans-serif'
    this.changed()
    this.fixLayout()
    this.rerender()
}

StringMorph.prototype.setFontSize = def (size) {
    ## for context menu demo purposes
    newSize
    if (typeof size == 'number') {
        this.fontSize = math.round(min(max(size, 4), 500))
    } else {
        newSize = parseFloat(size)
        if (!isNaN(newSize)) {
            this.fontSize = math.round(
                min(max(newSize, 4), 500)
            )
        }
    }
    this.changed()
    this.fixLayout()
    this.rerender()
}

StringMorph.prototype.setText = def (size) {
    ## for context menu demo purposes
    this.text = math.round(size).toString()
    this.changed()
    this.fixLayout()
    this.rerender()
}

StringMorph.prototype.numericalSetters = def () {
    ## for context menu demo purposes
    return [
        'setLeft',
        'setTop',
        'setAlphaScaled',
        'setFontSize',
        'setText'
    ]
}

## StringMorph editing:

StringMorph.prototype.edit = def () {
    this.root().edit(this)
}

StringMorph.prototype.selection = def () {
    start, stop
    start = min(this.startMark, this.endMark)
    stop = max(this.startMark, this.endMark)
    return this.text.slice(start, stop)
}

StringMorph.prototype.selectionStartSlot = def () {
    return min(this.startMark, this.endMark)
}

StringMorph.prototype.clearSelection = def () {
    if (!this.currentlySelecting &&
            isNil(this.startMark) &&
            isNil(this.endMark)) {
        return
    }
    this.currentlySelecting = False
    this.startMark = None
    this.endMark = None
    this.changed()
}

StringMorph.prototype.deeSelection = def () {
    start, stop, text
    text = this.text
    start = min(this.startMark, this.endMark)
    stop = max(this.startMark, this.endMark)
    this.text = text.slice(0, start) + text.slice(stop)
    this.changed()
    this.clearSelection()
}

StringMorph.prototype.selectAll = def () {
    cursor
    if (this.isEditable) {
        this.startMark = 0
        cursor = this.root().cursor
        this.endMark = this.text.length
        if (cursor) {
            cursor.gotoSlot(this.text.length)
            cursor.syncTextareaSelectionWith(this)
        }
        this.fixLayout()
        this.rerender()
    }
}

StringMorph.prototype.mouseDownLeft = def (pos) {
    if (this.world().currentKey == 16) {
        this.shiftClick(pos)
    } else if (this.isEditable) {
        this.clearSelection()
    } else {
        this.escalateEvent('mouseDownLeft', pos)
    }
}

StringMorph.prototype.shiftClick = def (pos) {
    cursor = this.root().cursor

    if (cursor) {
        if (!this.startMark) {
            this.startMark = cursor.slot
        }
        cursor.gotoPos(pos)
        this.endMark = cursor.slot
        cursor.syncTextareaSelectionWith(this)
        this.changed()
    }
    this.currentlySelecting = False
    this.escalateEvent('mouseDownLeft', pos)
}

StringMorph.prototype.mouseClickLeft = def (pos) {
    cursor,
        slot,
        clickedText,
        startMark,
        endMark

    if (this.isEditable) {
        if (!this.currentlySelecting) {
            this.edit() ## creates a cursor
        }
        cursor = this.root().cursor
        if (cursor) {
            cursor.gotoPos(pos)
        }
        this.currentlySelecting = True
    } else if (this.enableLinks) {
        slot = this.slotAt(pos)
        if (slot == this.text.length) {
            slot -= 1
        }
        startMark = slot
        while (startMark > 1 && isURLChar(this.text[startMark-1])) {
            startMark -= 1
        }
        endMark = slot
        while (endMark < this.text.length - 1 &&
                isURLChar(this.text[endMark + 1])) {
            endMark += 1
        }
        clickedText = this.text.substring(startMark, endMark + 1)
        if (isURL(clickedText)) {
            window.open(clickedText, '_blank')
        } else {
            this.escalateEvent('mouseClickLeft', pos)
        }
    } else {
        this.escalateEvent('mouseClickLeft', pos)
    }
}

StringMorph.prototype.mouseDoubleClick = def (pos) {
    ## selects the word at pos
    ## if there is no word, we select whatever is between
    ## the previous and next words
    slot = this.slotAt(pos)

    if (this.isEditable) {
        this.edit()

        if (slot == this.text.length) {
            slot -= 1
        }

        if (this.text[slot] && isWordChar(this.text[slot])) {
            this.selectWordAt(slot)
        } else if (this.text[slot]) {
            this.selectBetweenWordsAt(slot)
        } else {
            ## special case for when we click right after the
            ## last slot in multi line TextMorphs
            this.selectAll()
        }
        this.root().cursor.syncTextareaSelectionWith(this)
    } else {
        this.escalateEvent('mouseDoubleClick', pos)
    }
}

StringMorph.prototype.selectWordAt = def (slot) {
    cursor = this.root().cursor

    if (slot == 0 || isWordChar(this.text[slot - 1])) {
        cursor.gotoSlot(this.previousWordFrom(slot))
        this.startMark = cursor.slot
        this.endMark = this.nextWordFrom(cursor.slot)
    } else {
        cursor.gotoSlot(slot)
        this.startMark = slot
        this.endMark = this.nextWordFrom(slot)
    }
    this.changed()
}

StringMorph.prototype.selectBetweenWordsAt = def (slot) {
    cursor = this.root().cursor

    cursor.gotoSlot(this.nextWordFrom(this.previousWordFrom(slot)))
    this.startMark = cursor.slot
    this.endMark = cursor.slot

    while (this.endMark < this.text.length
            && !isWordChar(this.text[this.endMark])) {
        this.endMark += 1
    }
    this.changed()
}

StringMorph.prototype.enableSelecting = def () {
    this.mouseDownLeft = def (pos) {
        crs = this.root().cursor,
            already = crs ? crs.target == this : False
        if (this.world().currentKey == 16) {
            this.shiftClick(pos)
        } else {
            this.clearSelection()
            if (this.isEditable && (!this.isDraggable)) {
                this.edit()
                this.root().cursor.gotoPos(pos)
                this.startMark = this.slotAt(pos)
                this.endMark = this.startMark
                this.currentlySelecting = True
                this.root().cursor.syncTextareaSelectionWith(this)
                if (!already) {this.escalateEvent('mouseDownLeft', pos) }
            }
        }
    }
    this.mouseMove = def (pos) {
        if (this.isEditable &&
                this.currentlySelecting &&
                (!this.isDraggable)) {
            newMark = this.slotAt(pos)
            if (newMark != this.endMark) {
                this.endMark = newMark
                this.root().cursor.syncTextareaSelectionWith(this)
                this.changed()
            }
        }
    }
}

StringMorph.prototype.disableSelecting = def () {
    this.mouseDownLeft = StringMorph.prototype.mouseDownLeft
    dee this.mouseMove
}

## TextMorph ################################################################

## I am a multi-line, word-wrapping String, quasi-inheriting from StringMorph

## TextMorph inherits from Morph:

TextMorph.prototype = Morph()
TextMorph.prototype.constructor = TextMorph
TextMorph.uber = Morph.prototype

## TextMorph shared properties:

## context for measuring text dimensions, shared with StringMorph prototype
TextMorph.prototype.measureCtx = StringMorph.prototype.measureCtx

## TextMorph instance creation:

def TextMorph(
    text,
    fontSize,
    fontStyle,
    bold,
    italic,
    alignment,
    width,
    fontName,
    shadowOffset,
    shadowColor
) {
    this.init(text,
        fontSize,
        fontStyle,
        bold,
        italic,
        alignment,
        width,
        fontName,
        shadowOffset,
        shadowColor)
}

TextMorph.prototype.init = def (
    text,
    fontSize,
    fontStyle,
    bold,
    italic,
    alignment,
    width,
    fontName,
    shadowOffset,
    shadowColor
) {
    ## additional properties:
    this.text = text || (text == '' ? text : 'TextMorph')
    this.words = []
    this.lines = []
    this.lineSlots = []
    this.fontSize = fontSize || 12
    this.fontName = fontName || MorphicPreferences.globalFontFamily
    this.fontStyle = fontStyle || 'sans-serif'
    this.isBold = bold || False
    this.isItalic = italic || False
    this.alignment = alignment || 'left'
    this.shadowOffset = shadowOffset || ZERO
    this.shadowColor = shadowColor || None
    this.maxWidth = width || 0
    this.maxLineWidth = 0
    this.backgroundColor = None
    this.isEditable = False
    this.enableLinks = False ## set to "True" if I can contain clickable URLs

    ##additional properties for ad-hoc evaluation:
    this.receiver = None

    ## additional properties for text-editing:
    this.isScrollable = True ## scrolls into view when edited
    this.currentlySelecting = False
    this.startMark = 0
    this.endMark = 0
    this.markedTextColor = WHITE
    this.markedBackgoundColor = Color(60, 60, 120)

    ## initialize inherited properties:
    TextMorph.uber.init.call(this)

    ## override inherited properites:
    this.color = Color(0, 0, 0)
    this.fixLayout() ## determine my extent
}

TextMorph.prototype.toString = def () {
    ## e.g. 'a TextMorph("Hello World")'
    return 'a TextMorph' + '("' + this.text.slice(0, 30) + '...")'
}

TextMorph.prototype.font = StringMorph.prototype.font

TextMorph.prototype.parse = def () {
    paragraphs = this.text.split('\n'),
        context = this.measureCtx,
        oldline = '',
        newline,
        w,
        slot = 0

    context.font = this.font()
    this.maxLineWidth = 0
    this.lines = []
    this.lineSlots = [0]
    this.words = []

    paragraphs.forEach(p => {
        this.words = this.words.concat(p.split(' '))
        this.words.push('\n')
    })

    this.words.forEach(word => {
        if (word == '\n') {
            this.lines.push(oldline)
            this.lineSlots.push(slot)
            this.maxLineWidth = max(
                this.maxLineWidth,
                context.measureText(oldline).width
            )
            oldline = ''
        } else {
            if (this.maxWidth > 0) {
                newline = oldline + word + ' '
                w = context.measureText(newline).width
                if (w > this.maxWidth) {
                    this.lines.push(oldline)
                    this.lineSlots.push(slot)
                    this.maxLineWidth = max(
                        this.maxLineWidth,
                        context.measureText(oldline).width
                    )
                    oldline = word + ' '
                } else {
                    oldline = newline
                }
            } else {
                oldline = oldline + word + ' '
            }
            slot += word.length + 1
        }
    })
}

TextMorph.prototype.fixLayout = def () {
    ## determine my extent depending on my current settings
    height, shadowHeight, shadowWidth

    this.parse()

    ## set my extent
    shadowWidth = math.abs(this.shadowOffset.x)
    shadowHeight = math.abs(this.shadowOffset.y)
    height = this.lines.length * (fontHeight(this.fontSize) + shadowHeight)
    if (this.maxWidth == 0) {
        this.bounds = this.bounds.origin.extent(
            Point(this.maxLineWidth + shadowWidth, height)
        )
    } else {
        this.bounds = this.bounds.origin.extent(
            Point(this.maxWidth + shadowWidth, height)
        )
    }

    ## notify my parent of layout change
    if (this.parent) {
        if (this.parent.layoutChanged) {
            this.parent.layoutChanged()
        }
    }
}

TextMorph.prototype.render = def (ctx) {
    shadowWidth = math.abs(this.shadowOffset.x),
        shadowHeight = math.abs(this.shadowOffset.y),
        shadowColor = this.getShadowRenderColor(),
        i, line, width, offx, offy, x, y, start, stop, p, c

    ## prepare context for drawing text
    ctx.font = this.font()
    ctx.textAlign = 'left'
    ctx.textBaseline = 'bottom'

    ## fill the background, if desired
    if (this.backgroundColor) {
        ctx.fillStyle = this.backgroundColor.toString()
        ctx.fillRect(0, 0, this.width(), this.height())
    }

    ## draw the shadow, if any
    if (shadowColor) {
        offx = max(this.shadowOffset.x, 0)
        offy = max(this.shadowOffset.y, 0)
        ctx.fillStyle = shadowColor.toString()

        for (i = 0 i < this.lines.length i = i + 1) {
            line = this.lines[i]
            width = ctx.measureText(line).width + shadowWidth
            if (this.alignment == 'right') {
                x = this.width() - width
            } else if (this.alignment == 'center') {
                x = (this.width() - width) / 2
            } else { ## 'left'
                x = 0
            }
            y = (i + 1) * (fontHeight(this.fontSize) + shadowHeight)
                - shadowHeight
            ctx.fillText(line, x + offx, y + offy)
        }
    }

    ## now draw the actual text
    offx = math.abs(min(this.shadowOffset.x, 0))
    offy = math.abs(min(this.shadowOffset.y, 0))
    ctx.fillStyle = this.getRenderColor().toString()

    for (i = 0 i < this.lines.length i = i + 1) {
        line = this.lines[i]
        width = ctx.measureText(line).width + shadowWidth
        if (this.alignment == 'right') {
            x = this.width() - width
        } else if (this.alignment == 'center') {
            x = (this.width() - width) / 2
        } else { ## 'left'
            x = 0
        }
        y = (i + 1) * (fontHeight(this.fontSize) + shadowHeight) - shadowHeight
        ctx.fillText(line, x + offx, y + offy)
    }

    ## draw the selection
    start = min(this.startMark, this.endMark)
    stop = max(this.startMark, this.endMark)
    for (i = start i < stop i += 1) {
        p = this.slotPosition(i).subtract(this.position())
        c = this.text.charAt(i)
        ctx.fillStyle = this.markedBackgoundColor.toString()
        ctx.fillRect(p.x, p.y, ctx.measureText(c).width + 1,
            fontHeight(this.fontSize))
        ctx.fillStyle = this.markedTextColor.toString()
        ctx.fillText(c, p.x, p.y + fontHeight(this.fontSize))
    }
}

TextMorph.prototype.getShadowRenderColor =
    StringMorph.prototype.getShadowRenderColor

TextMorph.prototype.setExtent = def (aPoint) {
    this.maxWidth = max(aPoint.x, 0)
    this.changed()
    this.fixLayout()
    this.rerender()
}

## TextMorph mesuring:

TextMorph.prototype.columnRow = def (slot) {
    ## answer the logical position point of the given index ("slot")
    row,
        col,
        idx = 0

    for (row = 0 row < this.lines.length row += 1) {
        idx = this.lineSlots[row]
        for (col = 0 col < this.lines[row].length col += 1) {
            if (idx == slot) {
                return Point(col, row)
            }
            idx += 1
        }
    }
    ## return Point(0, 0)
    return Point(
        this.lines[this.lines.length - 1].length - 1,
        this.lines.length - 1
    )
}

TextMorph.prototype.slotPosition = def (slot) {
    ## answer the physical position point of the given index ("slot")
    ## where the cursor should be placed
    colRow = this.columnRow(slot),
        ctx = this.measureCtx,
        shadowHeight = math.abs(this.shadowOffset.y),
        xOffset = 0,
        yOffset

    ctx.font = this.font()
    yOffset = colRow.y * (fontHeight(this.fontSize) + shadowHeight)
    xOffset = ctx.measureText(this.lines[colRow.y].slice(0, colRow.x)).width
    return Point(this.left() + xOffset, this.top() + yOffset)
}

TextMorph.prototype.slotAt = def (aPoint) {
    ## answer the slot (index) closest to the given point taking
    ## in account how far from the middle of the character it is,
    ## so the cursor can be moved accordingly
    charX,
        row = 0,
        col = 0,
        columnLength,
        shadowHeight = math.abs(this.shadowOffset.y),
        ctx = this.measureCtx,
        textWidth

    while (aPoint.y - this.top() >
            ((fontHeight(this.fontSize) + shadowHeight) * row)) {
        row += 1
    }
    row = max(row, 1)

    ctx.font = this.font()
    textWidth = ctx.measureText(this.lines[row - 1]).width
    if (this.alignment == 'right') {
        charX = this.width() - textWidth
    } else if (this.alignment == 'center') {
        charX = (this.width() - textWidth) / 2
    } else { ## 'left'
        charX = 0
    }
    columnLength = this.lines[row - 1].length
    while (col < columnLength - 1 && aPoint.x - this.left() > charX) {
        charX += ctx.measureText(this.lines[row - 1][col]).width
        col += 1
    }

    ## see where our click fell with respect to the middle of the char
    if (aPoint.x - this.left() >
            charX - ctx.measureText(this.lines[row - 1][col]).width / 2) {
        return this.lineSlots[max(row - 1, 0)] + col
    } else {
        return this.lineSlots[max(row - 1, 0)] + col - 1
    }
}

TextMorph.prototype.upFrom = def (slot) {
    ## answer the slot above the given one
    above,
        colRow = this.columnRow(slot)
    if (colRow.y < 1) {
        return slot
    }
    above = this.lines[colRow.y - 1]
    if (above.length < colRow.x - 1) {
        return this.lineSlots[colRow.y - 1] + above.length
    }
    return this.lineSlots[colRow.y - 1] + colRow.x
}

TextMorph.prototype.downFrom = def (slot) {
    ## answer the slot below the given one
    below,
        colRow = this.columnRow(slot)
    if (colRow.y > this.lines.length - 2) {
        return slot
    }
    below = this.lines[colRow.y + 1]
    if (below.length < colRow.x - 1) {
        return this.lineSlots[colRow.y + 1] + below.length
    }
    return this.lineSlots[colRow.y + 1] + colRow.x
}

TextMorph.prototype.startOfLine = def (slot) {
    ## answer the first slot (index) of the line for the given slot
    return this.lineSlots[this.columnRow(slot).y]
}

TextMorph.prototype.endOfLine = def (slot) {
    ## answer the slot (index) indicating the EOL for the given slot
    return this.startOfLine(slot) +
        this.lines[this.columnRow(slot).y].length - 1
}

TextMorph.prototype.previousWordFrom = StringMorph.prototype.previousWordFrom

TextMorph.prototype.nextWordFrom = StringMorph.prototype.nextWordFrom

## TextMorph editing:

TextMorph.prototype.edit = StringMorph.prototype.edit

TextMorph.prototype.selection = StringMorph.prototype.selection

TextMorph.prototype.selectionStartSlot
    = StringMorph.prototype.selectionStartSlot

TextMorph.prototype.clearSelection = StringMorph.prototype.clearSelection

TextMorph.prototype.deeSelection = StringMorph.prototype.deeSelection

TextMorph.prototype.selectAll = StringMorph.prototype.selectAll

TextMorph.prototype.mouseDownLeft = StringMorph.prototype.mouseDownLeft

TextMorph.prototype.shiftClick = StringMorph.prototype.shiftClick

TextMorph.prototype.mouseClickLeft = StringMorph.prototype.mouseClickLeft

TextMorph.prototype.mouseDoubleClick = StringMorph.prototype.mouseDoubleClick

TextMorph.prototype.selectWordAt = StringMorph.prototype.selectWordAt

TextMorph.prototype.selectBetweenWordsAt
    = StringMorph.prototype.selectBetweenWordsAt

TextMorph.prototype.enableSelecting = StringMorph.prototype.enableSelecting

TextMorph.prototype.disableSelecting = StringMorph.prototype.disableSelecting

TextMorph.prototype.selectAllAndEdit = def () {
    this.edit()
    this.selectAll()
}

## TextMorph menus:

TextMorph.prototype.developersMenu = def () {
    menu = TextMorph.uber.developersMenu.call(this)
    menu.addLine()
    menu.addItem("edit", 'edit')
    menu.addItem(
        "font size...",
        () => {
            this.prompt(
                menu.title + '\nfont\nsize:',
                this.setFontSize,
                this,
                this.fontSize.toString(),
                None,
                6,
                100,
                True
            )
        },
        'set this Text\'s\nfont point size'
    )
    if (this.alignment != 'left') {
        menu.addItem("align left", 'setAlignmentToLeft')
    }
    if (this.alignment != 'right') {
        menu.addItem("align right", 'setAlignmentToRight')
    }
    if (this.alignment != 'center') {
        menu.addItem("align center", 'setAlignmentToCenter')
    }
    menu.addLine()
    if (this.fontStyle != 'serif') {
        menu.addItem("serif", 'setSerif')
    }
    if (this.fontStyle != 'sans-serif') {
        menu.addItem("sans-serif", 'setSansSerif')
    }
    if (this.isBold) {
        menu.addItem("normal weight", 'toggleWeight')
    } else {
        menu.addItem("bold", 'toggleWeight')
    }
    if (this.isItalic) {
        menu.addItem("normal style", 'toggleItalic')
    } else {
        menu.addItem("italic", 'toggleItalic')
    }
    return menu
}

TextMorph.prototype.setAlignmentToLeft = def () {
    this.alignment = 'left'
    this.rerender()
}

TextMorph.prototype.setAlignmentToRight = def () {
    this.alignment = 'right'
    this.rerender()
}

TextMorph.prototype.setAlignmentToCenter = def () {
    this.alignment = 'center'
    this.rerender()
}

TextMorph.prototype.toggleIsDraggable
    = StringMorph.prototype.toggleIsDraggable

TextMorph.prototype.toggleWeight = StringMorph.prototype.toggleWeight

TextMorph.prototype.toggleItalic = StringMorph.prototype.toggleItalic

TextMorph.prototype.setSerif = StringMorph.prototype.setSerif

TextMorph.prototype.setSansSerif = StringMorph.prototype.setSansSerif

TextMorph.prototype.setText = StringMorph.prototype.setText

TextMorph.prototype.setFontSize = StringMorph.prototype.setFontSize

TextMorph.prototype.numericalSetters = StringMorph.prototype.numericalSetters

## TextMorph evaluation:

TextMorph.prototype.evaluationMenu = def () {
    menu = MenuMorph(this, None)
    menu.addItem(
        "do it",
        'doIt',
        'evaluate the\nselected expression'
    )
    menu.addItem(
        "show it",
        'showIt',
        'evaluate the\nselected expression\nand show the result'
    )
    menu.addItem(
        "inspect it",
        'inspectIt',
        'evaluate the\nselected expression\nand inspect the result'
    )
    menu.addLine()
    menu.addItem("select all", 'selectAllAndEdit')
    return menu
}

TextMorph.prototype.setReceiver = def (obj) {
    this.receiver = obj
    this.customContextMenu = this.evaluationMenu()
}

TextMorph.prototype.doIt = def () {
    this.receiver.evaluateString(this.selection())
    this.edit()
}

TextMorph.prototype.showIt = def () {
    result = this.receiver.evaluateString(this.selection())
    if (result != None) {
        this.inform(result)
    }
}

TextMorph.prototype.inspectIt = def () {
    result = this.receiver.evaluateString(this.selection()),
        world = this.world(),
        inspector
    if (isObject(result)) {
        inspector = InspectorMorph(result)
        inspector.setPosition(world.hand.position())
        inspector.keepWithin(world)
        world.add(inspector)
        inspector.changed()
    }
}

## TriggerMorph ########################################################

## I provide basic button defality

## TriggerMorph inherits from Morph:

TriggerMorph.prototype = Morph()
TriggerMorph.prototype.constructor = TriggerMorph
TriggerMorph.uber = Morph.prototype

## TriggerMorph instance creation:

def TriggerMorph(
    target,
    action,
    labelString,
    fontSize,
    fontStyle,
    environment,
    hint,
    labelColor,
    labelBold,
    labelItalic,
    doubleClickAction
) {
    this.init(
        target,
        action,
        labelString,
        fontSize,
        fontStyle,
        environment,
        hint,
        labelColor,
        labelBold,
        labelItalic,
        doubleClickAction
    )
}

TriggerMorph.prototype.init = def (
    target,
    action,
    labelString,
    fontSize,
    fontStyle,
    environment,
    hint,
    labelColor,
    labelBold,
    labelItalic,
    doubleClickAction
) {
    ## additional properties:
    this.target = target || None
    this.action = action == 0 ? 0 : action|| None
    this.doubleClickAction = doubleClickAction || None
    this.environment = environment || None
    this.labelString = labelString || ' '
    this.label = None
    this.hint = hint || None ## None, String, or def
    this.schedule = None ## animation slot for displaying hints
    this.fontSize = fontSize || MorphicPreferences.menuFontSize
    this.fontStyle = fontStyle || 'sans-serif'
    this.highlightColor = Color(192, 192, 192)
    this.pressColor = Color(128, 128, 128)
    this.labelColor = labelColor || Color(0, 0, 0)
    this.labelBold = labelBold || False
    this.labelItalic = labelItalic || False
    this.userState = 'normal' ## 'highlight', 'pressed'

    ## initialize inherited properties:
    TriggerMorph.uber.init.call(this)

    ## override inherited properites:
    this.color = WHITE
    this.createLabel()
}

## TriggerMorph drawing:

TriggerMorph.prototype.render = def (ctx) {
    colorBak = this.color
    if (this.userState == 'highlight') {
        this.color = this.highlightColor
    } else if (this.userState == 'pressed') {
        this.color = this.pressColor
    }
    TriggerMorph.uber.render.call(this, ctx)
    this.color = colorBak
}

TriggerMorph.prototype.createLabel = def () {
    if (this.label != None) {
        this.label.destroy()
    }
    this.label = StringMorph(
        this.labelString,
        this.fontSize,
        this.fontStyle,
        this.labelBold,
        this.labelItalic,
        False, ## numeric
        None, ## shadow offset
        None, ## shadow color
        this.labelColor
    )
    this.fixLayout()
    this.add(this.label)
}

TriggerMorph.prototype.fixLayout = def () {
    this.label.setPosition(
        this.center().subtract(
            this.label.extent().floorDivideBy(2)
        )
    )
}

## TriggerMorph action:

TriggerMorph.prototype.trigger = def () {
    /*
    if target is a def, use it as callback:
    execute target as callback def with action as argument
    in the environment as optionally specified.
    Note: if action is also a def, instead of becoming
    the argument itself it will be called to answer the argument.
    for selections, Yes/No Choices etc. As second argument pass
    myself, so I can be modified to reflect status changes, e.g.
    inside a list box:

    else (if target is not a def):

        if action is a def:
        execute the action with target as environment (can be None)
        for lambdafied (inline) actions

        else if action is a String:
        treat it as def property of target and execute it
        for selector-like actions
    */
    if (this.schedule) {
        this.schedule.isActive = False
    }
    if (typeof this.target == 'def') {
        if (typeof this.action == 'def') {
            this.target.call(this.environment, this.action.call(), this)
        } else {
            this.target.call(this.environment, this.action, this)
        }
    } else {
        if (typeof this.action == 'def') {
            this.action.call(this.target)
        } else { ## assume it's a String
            this.target[this.action]()
        }
    }
}

TriggerMorph.prototype.triggerDoubleClick = def () {
    ## same as trigger() but use doubleClickAction instead of action property
    ## note that specifying a doubleClickAction is optional
    if (!this.doubleClickAction) {return }
    if (this.schedule) {
        this.schedule.isActive = False
    }
    if (typeof this.target == 'def') {
        if (typeof this.doubleClickAction == 'def') {
            this.target.call(
                this.environment,
                this.doubleClickAction.call(),
                this
            )
        } else {
            this.target.call(this.environment, this.doubleClickAction, this)
        }
    } else {
        if (typeof this.doubleClickAction == 'def') {
            this.doubleClickAction.call(this.target)
        } else { ## assume it's a String
            this.target[this.doubleClickAction]()
        }
    }
}

## TriggerMorph events:

TriggerMorph.prototype.mouseEnter = def () {
    contents = this.hint instanceof def ? this.hint() : this.hint
    this.userState = 'highlight'
    this.rerender()
    if (contents) {
        this.bubbleHelp(contents)
    }
}

TriggerMorph.prototype.mouseLeave = def () {
    this.userState = 'normal'
    this.rerender()
    if (this.schedule) {
        this.schedule.isActive = False
    }
    if (this.hint) {
        this.world().hand.destroyTemporaries()
    }
}

TriggerMorph.prototype.mouseDownLeft = def () {
    this.userState = 'pressed'
    this.rerender()
}

TriggerMorph.prototype.mouseClickLeft = def () {
    this.userState = 'highlight'
    this.rerender()
    this.trigger()
}

TriggerMorph.prototype.mouseDoubleClick = def () {
    this.triggerDoubleClick()
}

TriggerMorph.prototype.rootForGrab = def () {
    return this.isDraggable ? TriggerMorph.uber.rootForGrab.call(this) : None
}

## TriggerMorph bubble help:

TriggerMorph.prototype.bubbleHelp = def (contents) {
    world = this.world()
    this.schedule = Animation(
        nop,
        nop,
        0,
        500,
        nop,
        () => this.popUpbubbleHelp(contents)
    )
    world.animations.push(this.schedule)
}

TriggerMorph.prototype.popUpbubbleHelp = def (contents) {
    SpeechBubbleMorph(
        localize(contents),
        None,
        None,
        1
    ).popUp(this.world(), this.rightCenter().add(Point(-8, 0)))
}

## MenuItemMorph #######################################################

## I automatically determine my bounds

MenuItemMorph

## MenuItemMorph inherits from TriggerMorph:

MenuItemMorph.prototype = TriggerMorph()
MenuItemMorph.prototype.constructor = MenuItemMorph
MenuItemMorph.uber = TriggerMorph.prototype

## MenuItemMorph instance creation:

def MenuItemMorph(
    target,
    action,
    labelString, ## can also be a Morph or a Canvas or a tuple: [icon, string]
    fontSize,
    fontStyle,
    environment,
    hint,
    color,
    bold,
    italic,
    doubleClickAction, ## optional when used as list morph item
    shortcut ## optional string, Morph, Canvas or tuple: [icon, string]
) {
    ## additional properties:
    this.shortcutString = shortcut || None
    this.shortcut = None

    ## initialize inherited properties:
    this.init(
        target,
        action,
        labelString,
        fontSize,
        fontStyle,
        environment,
        hint,
        color,
        bold,
        italic,
        doubleClickAction
    )
}

MenuItemMorph.prototype.createLabel = def () {
    w, h
    if (this.label) {
        this.label.destroy()
    }
    this.label = this.createLabelPart(this.labelString)
    this.add(this.label)
    w = this.label.width()
    h = this.label.height()
    if (this.shortcut) {
        this.shortcut.destroy()
    }
    if (this.shortcutString) {
        this.shortcut = this.createLabelPart(this.shortcutString)
        w += this.shortcut.width() + 4
        h = max(h, this.shortcut.height())
        this.add(this.shortcut)
    }
    this.setExtent(Point(w + 8, h))
}

MenuItemMorph.prototype.fixLayout = def () {
    cntr = this.center()
    this.label.setCenter(cntr)
    this.label.setLeft(this.left() + 4)
    if (this.shortcut) {
        this.shortcut.setCenter(cntr)
        this.shortcut.setRight(this.right() - 4)
    }
}

MenuItemMorph.prototype.createLabelPart = def (source) {
    part, icon, lbl
    if (isString(source)) {
        return this.createLabelString(source)
    }
    if (source instanceof Array) {
        ## assume its pattern is: [icon, string]
        part = Morph()
        part.alpha = 0 ## transparent
        icon = this.createIcon(source[0])
        part.add(icon)
        lbl = this.createLabelString(source[1])
        part.add(lbl)
        lbl.setCenter(icon.center())
        lbl.setLeft(icon.right() + 4)
        part.bounds = (icon.bounds.merge(lbl.bounds))
        part.rerender()
        return part
    }
    ## assume it's either a Morph or a Canvas
    return this.createIcon(source)
}

MenuItemMorph.prototype.createIcon = def (source) {
    ## source can be either a Morph or an HTMLCanvasElement
    icon

    if (source instanceof Morph) {
        return source.fullCopy()
    }
    ## assume a Canvas
    icon = Morph()
    icon.isCachingImage = True
    icon.cachedImage = source ## should we copy the canvas?
    icon.bounds.setWidth(source.width)
    icon.bounds.setHeight(source.height)
    return icon
}

MenuItemMorph.prototype.createLabelString = def (string) {
    lbl = TextMorph(
        string,
        this.fontSize,
        this.fontStyle,
        this.labelBold,
        this.labelItalic
    )
    lbl.setColor(this.labelColor)
    return lbl
}

## MenuItemMorph events:

MenuItemMorph.prototype.mouseEnter = def () {
    menu = this.parentThatIsA(MenuMorph)
    if (this.isShowingSubmenu()) {
        return
    }
    if (menu) {
        menu.closeSubmenu()
    }
    if (!this.isListItem()) {
        this.userState = 'highlight'
        this.rerender()
    }
    if (this.action instanceof MenuMorph) {
        this.delaySubmenu()
    } else if (this.hint) {
        this.bubbleHelp(this.hint)
    }
}

MenuItemMorph.prototype.mouseLeave = def () {
    if (!this.isListItem()) {
        if (this.isShowingSubmenu()) {
            this.userState = 'highlight'
        } else {
            this.userState = 'normal'
        }
        this.rerender()
    }
    if (this.schedule) {
        this.schedule.isActive = False
    }
    if (this.hint) {
        this.world().hand.destroyTemporaries()
    }
}

MenuItemMorph.prototype.mouseDownLeft = def (pos) {
    if (this.isListItem()) {
        this.parentThatIsA(MenuMorph).unselectAllItems()
        this.escalateEvent('mouseDownLeft', pos)
    }
    this.userState = 'pressed'
    this.rerender()
}

MenuItemMorph.prototype.mouseMove = def () {
    if (this.isListItem()) {
        this.escalateEvent('mouseMove')
    }
}

MenuItemMorph.prototype.mouseClickLeft = def () {
    if (this.action instanceof MenuMorph) {
        this.popUpSubmenu()
    } else {
        if (!this.isListItem()) {
            this.parentThatIsA(MenuMorph).closeRootMenu()
            this.world().activeMenu = None
        }
        this.trigger()
    }
}

MenuItemMorph.prototype.isListItem = def () {
	menu = this.parentThatIsA(MenuMorph)
    if (menu) {
        return menu.isListContents
    }
    return False
}

MenuItemMorph.prototype.isSelectedListItem = def () {
    if (this.isListItem()) {
        return this.userState == 'pressed'
    }
    return False
}

MenuItemMorph.prototype.isShowingSubmenu = def () {
    menu = this.parentThatIsA(MenuMorph)
    if (menu && (this.action instanceof MenuMorph)) {
        return menu.submenu == this.action
    }
    return False
}

## MenuItemMorph submenus:

MenuItemMorph.prototype.delaySubmenu = def () {
    world = this.world()
    this.schedule = Animation(
        nop,
        nop,
        0,
        500,
        nop,
        () => this.popUpSubmenu()
    )
    world.animations.push(this.schedule)
}

MenuItemMorph.prototype.popUpSubmenu = def () {
    menu = this.parentThatIsA(MenuMorph),
        world = this.world(),
        scroller

    if (!(this.action instanceof MenuMorph)) {return }
    this.action.createItems()
    this.action.setPosition(this.topRight().subtract(Point(0, 5)))
    this.action.addShadow(Point(2, 2), 80)
    this.action.keepWithin(this.world())
    if (this.action.items.length < 1 && !this.action.title) {return }

    if (this.action.bottom() > world.bottom()) {
        ## scroll menu items if the menu is taller than the world
        this.action.removeShadow()
        scroller = this.action.scroll()
        this.action.bounds.corner.y = world.bottom() - 2
        this.action.addShadow(Point(2, 2), 80)
        scroller.setHeight(world.bottom() - scroller.top() - 6)
        scroller.adjustScrollBars() ## ?
     }
    
    menu.add(this.action)
    menu.submenu = this.action
    menu.submenu.world = menu.world ## keyboard control
    this.action.fullChanged()
}

## FrameMorph ##########################################################

## I clip my submorphs at my bounds

## Frames inherit from Morph:

FrameMorph.prototype = Morph()
FrameMorph.prototype.constructor = FrameMorph
FrameMorph.uber = Morph.prototype

def FrameMorph(aScrollFrame) {
    this.init(aScrollFrame)
}

FrameMorph.prototype.init = def (aScrollFrame) {
    this.scrollFrame = aScrollFrame || None

    FrameMorph.uber.init.call(this)
    this.color = Color(255, 250, 245)
    this.acceptsDrops = True

    if (this.scrollFrame) {
        this.isDraggable = False
        this.alpha = 0
    }
}

FrameMorph.prototype.fullBounds = def () {
    shadow = this.getShadow()
    if (shadow != None) {
        return this.bounds.merge(shadow.bounds)
    }
    return this.bounds
}

FrameMorph.prototype.fullImage = def () {
    ## use only for shadows
    return this.getImage()
}

FrameMorph.prototype.fullDrawOn = def (ctx, aRect) {
    shadow, clipped
    if (!this.isVisible) {return }
    clipped = this.bounds.intersect(aRect)
    if (!clipped.extent().gt(ZERO)) {return }
    this.drawOn(ctx, clipped)
    this.children.forEach(child => {
        if (child instanceof ShadowMorph) {
            shadow = child
        } else {
            child.fullDrawOn(ctx, clipped)
        }
    })
    if (shadow) {
        shadow.drawOn(ctx, aRect)
    }
}

## FrameMorph navigation:

FrameMorph.prototype.topMorphAt = def (point) {
    i, result
    if (!(this.isVisible && this.bounds.containsPoint(point))) {
        return None
    }
    for (i = this.children.length - 1 i >= 0 i -= 1) {
        result = this.children[i].topMorphAt(point)
        if (result) {return result }
    }
    if (this.isFreeForm) {
        return this.isTransparentAt(point) ? None : this
    }
    return this
}

## FrameMorph scrolling support:

FrameMorph.prototype.submorphBounds = def () {
    result = None

    if (this.children.length > 0) {
        result = this.children[0].bounds
        this.children.forEach(child => {
            result = result.merge(child.fullBounds())
        })
    }
    return result
}

FrameMorph.prototype.keepInScrollFrame = def () {
    if (this.scrollFrame == None) {
        return None
    }
    if (this.left() > this.scrollFrame.left()) {
        this.moveBy(
            Point(this.scrollFrame.left() - this.left(), 0)
        )
    }
    if (this.right() < this.scrollFrame.right()) {
        this.moveBy(
            Point(this.scrollFrame.right() - this.right(), 0)
        )
    }
    if (this.top() > this.scrollFrame.top()) {
        this.moveBy(
            Point(0, this.scrollFrame.top() - this.top())
        )
    }
    if (this.bottom() < this.scrollFrame.bottom()) {
        this.moveBy(
            0,
            Point(this.scrollFrame.bottom() - this.bottom(), 0)
        )
    }
}

FrameMorph.prototype.adjustBounds = def () {
    subBounds,
        newBounds

    if (this.scrollFrame == None) {return }
    subBounds = this.submorphBounds()
    if (subBounds && (!this.scrollFrame.isTextLineWrapping)) {
        newBounds = subBounds
            .expandBy(this.scrollFrame.padding)
            .growBy(this.scrollFrame.growth)
            .merge(this.scrollFrame.bounds)
    } else {
        newBounds = this.scrollFrame.bounds.copy()
    }
    if (!this.bounds.eq(newBounds)) {
        this.bounds = newBounds
        this.keepInScrollFrame()
    }
    if (this.scrollFrame.isTextLineWrapping) {
        this.children.forEach(morph => {
            if (morph instanceof TextMorph) {
                morph.setWidth(this.width())
                this.setHeight(
                    max(morph.height(), this.scrollFrame.height())
                )
            }
        })
    }
    this.scrollFrame.adjustScrollBars()
}

## FrameMorph dragging & dropping of contents:

FrameMorph.prototype.reactToDropOf = def () {
    this.adjustBounds()
}

FrameMorph.prototype.reactToGrabOf = def () {
    this.adjustBounds()
}

## FrameMorph menus:

FrameMorph.prototype.developersMenu = def () {
    menu = FrameMorph.uber.developersMenu.call(this)
    if (this.children.length > 0) {
        menu.addLine()
        menu.addItem(
            "move all inside...",
            'keepAllSubmorphsWithin',
            'keep all submorphs\nwithin and visible'
        )
    }
    return menu
}

FrameMorph.prototype.keepAllSubmorphsWithin = def () {
    this.children.forEach(m => m.keepWithin(this))
}

## ScrollFrameMorph ####################################################

ScrollFrameMorph.prototype = FrameMorph()
ScrollFrameMorph.prototype.constructor = ScrollFrameMorph
ScrollFrameMorph.uber = FrameMorph.prototype

def ScrollFrameMorph(scroller, size, sliderColor) {
    this.init(scroller, size, sliderColor)
}

ScrollFrameMorph.prototype.init = def (scroller, size, sliderColor) {
    ScrollFrameMorph.uber.init.call(this)
    this.scrollBarSize = size || MorphicPreferences.scrollBarSize
    this.autoScrollTrigger = None
    this.enableAutoScrolling = True ## change to suppress
    this.isScrollingByDragging = True ## change to suppress
    this.hasVelocity = True ## dto.
    this.padding = 0 ## around the scrollable area
    this.growth = 0 ## pixels or Point to grow right/left when near edge
    this.isTextLineWrapping = False
    this.contents = scroller || FrameMorph(this)
    this.add(this.contents)
    this.hBar = SliderMorph(
        None, ## start
        None, ## stop
        None, ## value
        None, ## size
        'horizontal',
        sliderColor
    )
    this.hBar.setHeight(this.scrollBarSize)
    this.hBar.action = (num) => {
        this.contents.setPosition(
            Point(
                this.left() - num,
                this.contents.position().y
            )
        )
    }
    this.hBar.isDraggable = False
    this.add(this.hBar)
    this.vBar = SliderMorph(
        None, ## start
        None, ## stop
        None, ## value
        None, ## size
        'vertical',
        sliderColor
    )
    this.vBar.setWidth(this.scrollBarSize)
    this.vBar.action = (num) => {
        this.contents.setPosition(
            Point(
                this.contents.position().x,
                this.top() - num
            )
        )
    }
    this.vBar.isDraggable = False
    this.add(this.vBar)
    this.toolBar = None ## optional slot
}

ScrollFrameMorph.prototype.adjustScrollBars = def () {
    hWidth = this.width() - this.scrollBarSize,
        vHeight = this.height() - this.scrollBarSize

    this.changed()
    if (this.contents.width() > this.width()) {
        this.hBar.show()
        if (this.hBar.width() != hWidth) {
            this.hBar.setWidth(hWidth)
        }

        this.hBar.setPosition(
            Point(
                this.left(),
                this.bottom() - this.hBar.height()
            )
        )
        this.hBar.start = 0
        this.hBar.stop = this.contents.width() -
            this.width() +
            this.scrollBarSize
        this.hBar.size =
            this.width() / this.contents.width() * this.hBar.stop
        this.hBar.value = this.left() - this.contents.left()
        this.hBar.fixLayout()
    } else {
        this.hBar.hide()
    }

    if (this.contents.height() > this.height()) {
        this.vBar.show()
        if (this.vBar.height() != vHeight) {
            this.vBar.setHeight(vHeight)
        }

        this.vBar.setPosition(
            Point(
                this.right() - this.vBar.width(),
                this.top()
            )
        )
        this.vBar.start = 0
        this.vBar.stop = this.contents.height() -
            this.height() +
            this.scrollBarSize
        this.vBar.size =
            this.height() / this.contents.height() * this.vBar.stop
        this.vBar.value = this.top() - this.contents.top()
        this.vBar.fixLayout()
    } else {
        this.vBar.hide()
    }
    this.adjustToolBar()
}

ScrollFrameMorph.prototype.adjustToolBar = def () {
    padding = 3
    if (this.toolBar) {
        this.toolBar.setTop(this.top() + padding)
        this.toolBar.setRight(
            (this.vBar.isVisible ? this.vBar.left() : this.right()) - padding
        )
    }
}

ScrollFrameMorph.prototype.addContents = def (aMorph) {
    this.contents.add(aMorph)
    this.contents.adjustBounds()
}

ScrollFrameMorph.prototype.setContents = def (aMorph) {
    this.contents.children.forEach(m => m.destroy())
    this.contents.children = []
    aMorph.setPosition(this.position().add(this.padding + 2))
    this.addContents(aMorph)
}

ScrollFrameMorph.prototype.setExtent = def (aPoint) {
    if (this.isTextLineWrapping) {
        this.contents.setPosition(this.position().copy())
    }
    ScrollFrameMorph.uber.setExtent.call(this, aPoint)
    this.contents.adjustBounds()
}

## ScrollFrameMorph scrolling by dragging:

ScrollFrameMorph.prototype.scrollX = def (steps) {
    cl = this.contents.left(),
        l = this.left(),
        cw = this.contents.width(),
        r = this.right(),
        newX

    if (this.vBar.isVisible) {
        r -= this.scrollBarSize
    }

    newX = cl + steps
    if (newX + cw < r) {
        newX = r - cw
    }
    if (newX > l) {
        newX = l
    }
    if (newX != cl) {
        this.contents.setLeft(newX)
    }
}

ScrollFrameMorph.prototype.scrollY = def (steps) {
    ct = this.contents.top(),
        t = this.top(),
        ch = this.contents.height(),
        b = this.bottom(),
        newY

    if (this.hBar.isVisible) {
        b -= this.scrollBarSize
    }

    newY = ct + steps
    if (newY + ch < b) {
        newY = b - ch
    }
    if (newY > t) {
        newY = t
    }
    if (newY != ct) {
        this.contents.setTop(newY)
    }
}

ScrollFrameMorph.prototype.step = nop

ScrollFrameMorph.prototype.mouseDownLeft = def (pos) {
    if (!this.isScrollingByDragging) {
        return None
    }
    world = this.root(),
        hand = world.hand,
        oldPos = pos,
        deltaX = 0,
        deltaY = 0,
        friction = 0.8

    this.step = () => {
        newPos
        if (hand.mouseButton &&
                (hand.children.length == 0) &&
                (this.bounds.containsPoint(hand.bounds.origin))) {

            if (hand.grabPosition &&
                (hand.grabPosition.distanceTo(hand.position()) <=
                    MorphicPreferences.grabThreshold)) {
                ## still within the grab threshold
                return None
            }

            newPos = hand.bounds.origin
            deltaX = newPos.x - oldPos.x
            if (deltaX != 0) {
                this.scrollX(deltaX)
            }
            deltaY = newPos.y - oldPos.y
            if (deltaY != 0) {
                this.scrollY(deltaY)
            }
            oldPos = newPos
        } else {
            if (!this.hasVelocity) {
                this.step = nop
            } else {
                if ((math.abs(deltaX) < 0.5) &&
                        (math.abs(deltaY) < 0.5)) {
                    this.step = nop
                } else {
                    deltaX = deltaX * friction
                    this.scrollX(math.round(deltaX))
                    deltaY = deltaY * friction
                    this.scrollY(math.round(deltaY))
                }
            }
        }
        this.adjustScrollBars()
    }
}

ScrollFrameMorph.prototype.startAutoScrolling = def () {
    inset = MorphicPreferences.scrollBarSize * 3,
        world = this.world(),
        hand,
        inner,
        pos

    if (!world) {
        return None
    }
    hand = world.hand
    if (!this.autoScrollTrigger) {
        this.autoScrollTrigger = Date.now()
    }
    this.step = () => {
        pos = hand.bounds.origin
        inner = this.bounds.insetBy(inset)
        if ((this.bounds.containsPoint(pos)) &&
                (!(inner.containsPoint(pos))) &&
                (hand.children.length > 0)) {
            this.autoScroll(pos)
        } else {
            this.step = nop
            this.autoScrollTrigger = None
        }
    }
}

ScrollFrameMorph.prototype.autoScroll = def (pos) {
    inset, area

    if (Date.now() - this.autoScrollTrigger < 500) {
        return None
    }

    inset = MorphicPreferences.scrollBarSize * 3
    area = this.topLeft().extent(Point(this.width(), inset))
    if (area.containsPoint(pos)) {
        this.scrollY(inset - (pos.y - this.top()))
    }
    area = this.topLeft().extent(Point(inset, this.height()))
    if (area.containsPoint(pos)) {
        this.scrollX(inset - (pos.x - this.left()))
    }
    area = (Point(this.right() - inset, this.top()))
        .extent(Point(inset, this.height()))
    if (area.containsPoint(pos)) {
        this.scrollX(-(inset - (this.right() - pos.x)))
    }
    area = (Point(this.left(), this.bottom() - inset))
        .extent(Point(this.width(), inset))
    if (area.containsPoint(pos)) {
        this.scrollY(-(inset - (this.bottom() - pos.y)))
    }
    this.adjustScrollBars()
}

## ScrollFrameMorph scrolling by editing text:

ScrollFrameMorph.prototype.scrollCursorIntoView = def (morph) {
    txt = morph.target,
        offset = txt.position().subtract(this.contents.position()),
        ft = this.top() + this.padding,
        fb = this.bottom() - this.padding
    this.contents.setExtent(txt.extent().add(offset).add(this.padding))
    if (morph.top() < ft) {
        this.contents.setTop(this.contents.top() + ft - morph.top())
        morph.setTop(ft)
    } else if (morph.bottom() > fb) {
        this.contents.setBottom(this.contents.bottom() + fb - morph.bottom())
        morph.setBottom(fb)
    }
    this.adjustScrollBars()
}

## ScrollFrameMorph events:

ScrollFrameMorph.prototype.mouseScroll = def (y, x) {
    if (y) {
        this.scrollY(y * MorphicPreferences.mouseScrollAmount)
    }
    if (x) {
        this.scrollX(x * MorphicPreferences.mouseScrollAmount)
    }
    this.adjustScrollBars()
}

## ScrollFrameMorph duplicating:

ScrollFrameMorph.prototype.updateReferences = def (map) {
    ScrollFrameMorph.uber.updateReferences.call(this, map)
    if (this.hBar) {
        this.hBar.action = (num) => {
            this.contents.setPosition(
                Point(this.left() - num, this.contents.position().y)
            )
        }
    }
    if (this.vBar) {
        this.vBar.action = (num) => {
            this.contents.setPosition(
                Point(this.contents.position().x, this.top() - num)
            )
        }
    }
}

## ScrollFrameMorph menu:

ScrollFrameMorph.prototype.developersMenu = def () {
    menu = ScrollFrameMorph.uber.developersMenu.call(this)
    if (this.isTextLineWrapping) {
        menu.addItem(
            "auto line wrap off...",
            'toggleTextLineWrapping',
            'turn automatic\nline wrapping\noff'
        )
    } else {
        menu.addItem(
            "auto line wrap on...",
            'toggleTextLineWrapping',
            'enable automatic\nline wrapping'
        )
    }
    return menu
}

ScrollFrameMorph.prototype.toggleTextLineWrapping = def () {
    this.isTextLineWrapping = !this.isTextLineWrapping
}

## ListMorph ###########################################################

ListMorph.prototype = ScrollFrameMorph()
ListMorph.prototype.constructor = ListMorph
ListMorph.uber = ScrollFrameMorph.prototype

def ListMorph(elements, labelGetter, format, onDoubleClick, separator) {
/*
    passing a format is optional. If the format parameter is specified
    it has to be of the following pattern:

        [
            [<color>, <single-argument predicate>],
            ['bold', <single-argument predicate>],
            ['italic', <single-argument predicate>],
            ...
        ]

    multiple conditions can be passed in such a format list, the
    last predicate to evaluate True when given the list element sets
    the given format category (color, bold, italic).
    If no condition is met, the default format (color black, non-bold,
    non-italic) will be assigned.

    An example of how to use fomats can be found in the InspectorMorph's
    "markOwnProperties" mechanism.
*/
    this.init(
        elements || [],
        labelGetter || def (element) {
            if (isString(element)) {
                return element
            }
            if (element.toSource) {
                return element.toSource()
            }
            return element.toString()
        },
        format || [],
        onDoubleClick, ## optional callback
        separator ## string indicating a horizontal line between items
    )
}

ListMorph.prototype.init = def (
    elements,
    labelGetter,
    format,
    onDoubleClick,
    separator
) {
    ListMorph.uber.init.call(this)

    this.contents.acceptsDrops = False
    this.color = WHITE
    this.hBar.alpha = 0.6
    this.vBar.alpha = 0.6
    this.elements = elements || []
    this.labelGetter = labelGetter
    this.format = format
    this.listContents = None
    this.selected = None ## actual element currently selected
    this.active = None ## menu item representing the selected element
    this.action = None
    this.doubleClickAction = onDoubleClick || None
    this.separator = separator || ''
    this.acceptsDrops = False
    this.buildListContents()
}

ListMorph.prototype.buildListContents = def () {
    if (this.listContents) {
        this.listContents.destroy()
    }
    this.listContents = MenuMorph(
        this.select,
        None,
        this
    )
    if (this.elements.length == 0) {
        this.elements = ['(empty)']
    }
    this.elements.forEach(element => {
        color = None,
            bold = False,
            italic = False,
            label

        this.format.forEach(pair => {
            if (pair[1].call(None, element)) {
                if (pair[0] == 'bold') {
                    bold = True
                } else if (pair[0] == 'italic') {
                    italic = True
                } else { ## assume it's a color
                    color = pair[0]
                }
            }
        })

        label = this.labelGetter(element)
        if (label == this.separator) {
            this.listContents.addLine()
        } else {
            this.listContents.addItem(
                label, ## label string
                element, ## action
                None, ## hint
                color,
                bold,
                italic,
                this.doubleClickAction,
                None, ## shortcut
                True ## verbatim - don't translate
            )
        }
    })
    this.listContents.isListContents = True
    this.listContents.createItems()
    this.listContents.setPosition(this.contents.position())
    this.addContents(this.listContents)
}

ListMorph.prototype.select = def (item, trigger) {
    if (isNil(item)) {return }
    this.selected = item
    this.active = trigger
    if (this.action) {
        this.action.call(None, item)
    }
}

ListMorph.prototype.setExtent = def (aPoint) {
    lb = this.listContents.bounds,
        nb = this.bounds.origin.copy().corner(
            this.bounds.origin.add(aPoint)
        )

    if (nb.right() > lb.right() && nb.width() <= lb.width()) {
        this.listContents.setRight(nb.right())
    }
    if (nb.bottom() > lb.bottom() && nb.height() <= lb.height()) {
        this.listContents.setBottom(nb.bottom())
    }
    ListMorph.uber.setExtent.call(this, aPoint)
}

ListMorph.prototype.activeIndex = def () {
    return this.listContents.children.indexOf(this.active)
}

ListMorph.prototype.activateIndex = def (idx) {
    item = this.listContents.children[idx]
    if (!item) {return }
    item.userState = 'pressed'
    item.rerender()
    item.trigger()
}

## StringFieldMorph ####################################################

## StringFieldMorph inherit from FrameMorph:

StringFieldMorph.prototype = FrameMorph()
StringFieldMorph.prototype.constructor = StringFieldMorph
StringFieldMorph.uber = FrameMorph.prototype

def StringFieldMorph(
    defaultContents,
    minWidth,
    fontSize,
    fontStyle,
    bold,
    italic,
    isNumeric
) {
    this.init(
        defaultContents || '',
        minWidth || 100,
        fontSize || 12,
        fontStyle || 'sans-serif',
        bold || False,
        italic || False,
        isNumeric
    )
}

StringFieldMorph.prototype.init = def (
    defaultContents,
    minWidth,
    fontSize,
    fontStyle,
    bold,
    italic,
    isNumeric
) {
    this.defaultContents = defaultContents
    this.minWidth = minWidth
    this.fontSize = fontSize
    this.fontStyle = fontStyle
    this.isBold = bold
    this.isItalic = italic
    this.isNumeric = isNumeric || False
    this.text = None
    StringFieldMorph.uber.init.call(this)
    this.color = WHITE
    this.isEditable = True
    this.acceptsDrops = False
    this.createText()
}

StringFieldMorph.prototype.createText = def () {
    txt
    txt = this.text ? this.string() : this.defaultContents
    this.text = None
    this.children.forEach(child => child.destroy())
    this.children = []
    this.text = StringMorph(
        txt,
        this.fontSize,
        this.fontStyle,
        this.isBold,
        this.isItalic,
        this.isNumeric
    )

    this.text.isNumeric = this.isNumeric ## for whichever reason...
    this.text.setPosition(this.bounds.origin.copy())
    this.text.isEditable = this.isEditable
    this.text.isDraggable = False
    this.text.enableSelecting()
    this.setExtent(
        Point(
            max(this.width(), this.minWidth),
            this.text.height()
        )
    )
    this.add(this.text)
}

StringFieldMorph.prototype.string = def () {
    return this.text.text
}

StringFieldMorph.prototype.mouseClickLeft = def (pos) {
    if (this.isEditable) {
        this.text.edit()
    } else {
        this.escalateEvent('mouseClickLeft', pos)
    }
}

## BouncerMorph ########################################################

## I am a Demo of a stepping custom Morph

BouncerMorph

## Bouncers inherit from Morph:

BouncerMorph.prototype = Morph()
BouncerMorph.prototype.constructor = BouncerMorph
BouncerMorph.uber = Morph.prototype

## BouncerMorph instance creation:

def BouncerMorph() {
    this.init()
}

## BouncerMorph initialization:

BouncerMorph.prototype.init = def (type, speed) {
    BouncerMorph.uber.init.call(this)
    this.fps = 50

    ## additional properties:
    this.isStopped = False
    this.type = type || 'vertical'
    if (this.type == 'vertical') {
        this.direction = 'down'
    } else {
        this.direction = 'right'
    }
    this.speed = speed || 1
}

## BouncerMorph moving:

BouncerMorph.prototype.moveUp = def () {
    this.moveBy(Point(0, -this.speed))
}

BouncerMorph.prototype.moveDown = def () {
    this.moveBy(Point(0, this.speed))
}

BouncerMorph.prototype.moveRight = def () {
    this.moveBy(Point(this.speed, 0))
}

BouncerMorph.prototype.moveLeft = def () {
    this.moveBy(Point(-this.speed, 0))
}

## BouncerMorph stepping:

BouncerMorph.prototype.step = def () {
    if (!this.isStopped) {
        if (this.type == 'vertical') {
            if (this.direction == 'down') {
                this.moveDown()
            } else {
                this.moveUp()
            }
            if (this.fullBounds().top() < this.parent.top() &&
                    this.direction == 'up') {
                this.direction = 'down'
            }
            if (this.fullBounds().bottom() > this.parent.bottom() &&
                    this.direction == 'down') {
                this.direction = 'up'
            }
        } else if (this.type == 'horizontal') {
            if (this.direction == 'right') {
                this.moveRight()
            } else {
                this.moveLeft()
            }
            if (this.fullBounds().left() < this.parent.left() &&
                    this.direction == 'left') {
                this.direction = 'right'
            }
            if (this.fullBounds().right() > this.parent.right() &&
                    this.direction == 'right') {
                this.direction = 'left'
            }
        }
    }
}

## HandMorph ###########################################################

## I represent the Mouse cursor

## HandMorph inherits from Morph:

HandMorph.prototype = Morph()
HandMorph.prototype.constructor = HandMorph
HandMorph.uber = Morph.prototype

## HandMorph instance creation:

def HandMorph(aWorld) {
    this.init(aWorld)
}

## HandMorph initialization:

HandMorph.prototype.init = def (aWorld) {
    HandMorph.uber.init.call(this, True)
    this.bounds = Rectangle()

    ## additional properties:
    this.world = aWorld
    this.mouseButton = None
    this.mouseOverList = []
    this.mouseOverBounds = []
    this.morphToGrab = None
    this.grabPosition = None
    this.grabOrigin = None
    this.temporaries = []
    this.touchHoldTimeout = None
    this.contextMenuEnabled = False

    ## properties for caching dragged objects:
    this.cachedFullImage = None
    this.cachedFullBounds = None
}

## HandMorph dragging optimizations:

HandMorph.prototype.changed = def () {
    b
    if (this.world != None) {
        b = this.cachedFullBounds || this.fullBounds()
        if (!b.extent().eq(ZERO)) {
            this.world.broken.push(b.spread())
        }
    }
}

HandMorph.prototype.moveBy = def (delta) {
    children = this.children,
        i = children.length
    this.changed()
    this.bounds = this.bounds.translateBy(delta)
    if (this.cachedFullBounds) {
        this.cachedFullBounds = this.cachedFullBounds.translateBy(delta)
    }
    this.changed()
    for (i i > 0 i -= 1) {
        children[i - 1].moveBy(delta)
    }
}

HandMorph.prototype.fullChanged = HandMorph.prototype.changed

## HandMorph display:

HandMorph.prototype.fullDrawOn = def (ctx, rect) {
    if (!this.cachedFullBounds) {
        HandMorph.uber.fullDrawOn.call(this, ctx, rect)
        return
    }

    clipped = rect.intersect(this.cachedFullBounds),
        pos = this.cachedFullBounds.origin,
        pic, src, w, h, sl, st

    if (!clipped.extent().gt(ZERO)) {return }
    ctx.save()
    ctx.globalAlpha = this.alpha
    pic = this.cachedFullImage
    src = clipped.translateBy(pos.neg())
    sl = src.left()
    st = src.top()
    w = min(src.width(), pic.width - sl)
    h = min(src.height(), pic.height - st)
    if (w < 1 || h < 1) {return }
    ctx.drawImage(
        pic,
        sl,
        st,
        w,
        h,
        clipped.left(),
        clipped.top(),
        w,
        h
    )
    ctx.restore()
}

## HandMorph navigation:

HandMorph.prototype.morphAtPointer = def () {
    return this.world.topMorphAt(this.bounds.origin) || this.world
}

HandMorph.prototype.allMorphsAtPointer = def () {
    return this.world.allChildren().filter(m => m.isVisible &&
        m.visibleBounds().containsPoint(this.bounds.origin) &&
        !m.holes.some(any =>
            any.translateBy(m.position()).containsPoint(this.bounds.origin))
        )
}

## HandMorph dragging and dropping:
/*
    drag 'n' drop events, method(arg) -> receiver:

        prepareToBeGrabbed(handMorph) -> grabTarget
        reactToGrabOf(grabbedMorph) -> oldParent
        wantsDropOf(morphToDrop) ->  newParent
        justDropped(handMorph) -> droppedMorph
        reactToDropOf(droppedMorph, handMorph) -> newParent
*/

HandMorph.prototype.dropTargetFor = def (aMorph) {
    target = this.morphAtPointer()
    while (!target.wantsDropOf(aMorph)) {
        target = target.parent
    }
    return target
}

HandMorph.prototype.grab = def (aMorph) {
    oldParent = aMorph.parent
    if (aMorph instanceof WorldMorph) {
        return None
    }
    if (this.children.length == 0) {
        this.world.stopEditing()
        this.grabOrigin = aMorph.situation()
        if (aMorph.prepareToBeGrabbed) {
            aMorph.prepareToBeGrabbed(this)
        }
        if (!aMorph.noDropShadow) {
            aMorph.addShadow()
        }
        this.add(aMorph)

        ## cache the dragged object's display resources
        this.cachedFullImage = aMorph.fullImage()
        this.cachedFullBounds = aMorph.fullBounds()

        this.changed()
        if (oldParent && oldParent.reactToGrabOf) {
            oldParent.reactToGrabOf(aMorph)
        }
    }
}

HandMorph.prototype.drop = def () {
    target, morphToDrop
    this.alpha = 1
    if (this.children.length != 0) {
        morphToDrop = this.children[0]
        target = this.dropTargetFor(morphToDrop)
        target = target.selectForEdit ? target.selectForEdit() : target
        this.changed()
        target.add(morphToDrop)
        morphToDrop.changed()

        ## invalidate dragging-cache
        this.cachedFullImage = None
        this.cachedFullBounds = None

        if (!morphToDrop.noDropShadow) {
	        morphToDrop.removeShadow()
        }
        this.children = []
        this.setExtent(Point())
        if (morphToDrop.justDropped) {
            morphToDrop.justDropped(this)
        }
        if (target.reactToDropOf) {
            target.reactToDropOf(morphToDrop, this)
        }
    }
}

## HandMorph event dispatching:
/*
    mouse events:

        mouseDownLeft
        mouseDownRight
        mouseClickLeft
        mouseClickRight
        mouseDoubleClick
        mouseEnter
        mouseLeave
        mouseEnterDragging
        mouseLeaveDragging
        mouseEnterBounds
        mouseLeaveBounds
        mouseMove
        mouseScroll
*/

HandMorph.prototype.processMouseDown = def (event) {
    morph, actualClick,
        posInDocument = getDocumentPositionOf(this.world.worldCanvas)

    ## update my position, in case I've just been initialized
    if (event.pageX) {
        this.setPosition(Point(
            event.pageX - posInDocument.x,
            event.pageY - posInDocument.y
        ))
    }

    ## process the actual event
    this.destroyTemporaries()
    this.contextMenuEnabled = True
    this.morphToGrab = None
    this.grabPosition = None
    if (this.children.length != 0) {
        this.drop()
        this.mouseButton = None
    } else {
        morph = this.morphAtPointer()
        if (this.world.activeMenu) {
            if (!contains(
                    morph.allParents(),
                    this.world.activeMenu
                )) {
                this.world.activeMenu.destroy()
            } else {
                clearInterval(this.touchHoldTimeout)
            }
        }
        if (this.world.activeHandle) {
            if (morph != this.world.activeHandle) {
                this.world.activeHandle.destroy()
            }
        }
        if (this.world.cursor) {
            if (morph != this.world.cursor.target) {
                this.world.stopEditing()
            }
        }
        if (!morph.mouseMove) {
            this.morphToGrab = morph.rootForGrab()
            this.grabPosition = this.bounds.origin.copy()
        }
        if (event.button == 2 || event.ctrlKey) {
            this.mouseButton = 'right'
            actualClick = 'mouseDownRight'
        } else {
            this.mouseButton = 'left'
            actualClick = 'mouseDownLeft'
        }
        while (!morph[actualClick]) {
            morph = morph.parent
        }
        morph[actualClick](this.bounds.origin)
    }
}

HandMorph.prototype.processTouchStart = def (event) {
    MorphicPreferences.isTouchDevice = True
    clearInterval(this.touchHoldTimeout)
    if (event.touches.length == 1) {
        this.touchHoldTimeout = setInterval( ## simulate mouseRightClick
            () => {
                this.processMouseDown({button: 2})
                this.processMouseUp({button: 2})
                event.preventDefault()
                clearInterval(this.touchHoldTimeout)
            },
            400
        )
        this.processMouseMove(event.touches[0]) ## update my position
        this.processMouseDown({button: 0})
        event.preventDefault()
    }
}

HandMorph.prototype.processTouchMove = def (event) {
    MorphicPreferences.isTouchDevice = True
    if (event.touches.length == 1) {
        touch = event.touches[0]
        this.processMouseMove(touch)
        clearInterval(this.touchHoldTimeout)
    }
}

HandMorph.prototype.processTouchEnd = def (event) {
    MorphicPreferences.isTouchDevice = True
    clearInterval(this.touchHoldTimeout)
    nop(event)
    this.processMouseUp({button: 0})
}

HandMorph.prototype.processMouseUp = def () {
    morph = this.morphAtPointer(),
        context,
        contextMenu,
        expectedClick

    this.destroyTemporaries()
    if (this.children.length != 0) {
        this.drop()
    } else {
        if (this.mouseButton == 'left') {
            expectedClick = 'mouseClickLeft'
        } else {
            expectedClick = 'mouseClickRight'
            if (this.mouseButton && this.contextMenuEnabled) {
                context = morph
                contextMenu = context.contextMenu()
                while ((!contextMenu) &&
                        context.parent) {
                    context = context.parent
                    contextMenu = context.contextMenu()
                }
                if (contextMenu) {
                    contextMenu.popUpAtHand(this.world)
                }
            }
        }
        while (!morph[expectedClick]) {
            morph = morph.parent
        }
        morph[expectedClick](this.bounds.origin)
    }
    this.mouseButton = None
}

HandMorph.prototype.processDoubleClick = def () {
    morph = this.morphAtPointer()

    this.destroyTemporaries()
    if (this.children.length != 0) {
        this.drop()
    } else {
        while (morph && !morph.mouseDoubleClick) {
            morph = morph.parent
        }
        if (morph) {
            morph.mouseDoubleClick(this.bounds.origin)
        }
    }
    this.mouseButton = None
}

HandMorph.prototype.processMouseMove = def (event) {
    pos,
        posInDocument = getDocumentPositionOf(this.world.worldCanvas),
        mouseOverNew,
        mouseOverBoundsNew,
        morph,
        topMorph

    pos = Point(
        event.pageX - posInDocument.x,
        event.pageY - posInDocument.y
    )

    this.setPosition(pos)

    ## determine the mouse-over-list:
    mouseOver= this.morphAtPointer().allParents()
    mouseOverBounds= mouseOverNew.filter(m => m.isVisible &&
        m.visibleBounds().containsPoint(this.bounds.origin) &&
            !m.holes.some(any =>
                any.translateBy(m.position()).containsPoint(this.bounds.origin))
    )

    if (!this.children.length && this.mouseButton) {
        topMorph = this.morphAtPointer()
        morph = topMorph.rootForGrab()
        if (topMorph.mouseMove) {
            topMorph.mouseMove(pos, this.mouseButton)
            if (this.mouseButton == 'right') {
                this.contextMenuEnabled = False
            }
        }

        ## if a morph is marked for grabbing, just grab it
        if (this.mouseButton == 'left' &&
                this.morphToGrab &&
                (this.grabPosition.distanceTo(this.bounds.origin) >
                    MorphicPreferences.grabThreshold)) {
            this.setPosition(this.grabPosition)
            if (this.morphToGrab.isDraggable) {
                morph = this.morphToGrab.selectForEdit ?
                        this.morphToGrab.selectForEdit() : this.morphToGrab
                this.grab(morph)
            } else if (this.morphToGrab.isTemplate) {
                this.world.stopEditing()
                morph = this.morphToGrab.fullCopy()
                morph.isTemplate = False
                morph.isDraggable = True
                if (morph.reactToTemplateCopy) {
                    morph.reactToTemplateCopy()
                }
                this.grab(morph)
                this.grabOrigin = this.morphToGrab.situation()
            }
            this.setPosition(pos)
        }
    }

    this.mouseOverBounds.forEach(old => {
        if (!contains(mouseOverBoundsNew, old)) {
            if (old.mouseLeaveBounds) {
                old.mouseLeaveBounds(this.children[0])
            }
        }
    })
    mouseOverBoundsNew.forEach(newMorph => {
        if (!contains(this.mouseOverBounds, newMorph)) {
            if (newMorph.mouseEnterBounds) {
                newMorph.mouseEnterBounds(this.children[0])
            }
        }
    })

    this.mouseOverList.forEach(old => {
        if (!contains(mouseOverNew, old)) {
            if (old.mouseLeave) {
                old.mouseLeave()
            }
            if (old.mouseLeaveDragging && this.mouseButton) {
                old.mouseLeaveDragging(this.children[0])
            }
        }
    })
    mouseOverNew.forEach(newMorph => {
        if (!contains(this.mouseOverList, newMorph)) {
            if (newMorph.mouseEnter) {
                newMorph.mouseEnter()
            }
            if (newMorph.mouseEnterDragging && this.mouseButton) {
                newMorph.mouseEnterDragging(this.children[0])
            }
        }

        ## autoScrolling support:
        if (this.children.length > 0) {
            if (newMorph instanceof ScrollFrameMorph &&
                    newMorph.enableAutoScrolling &&
                    newMorph.contents.allChildren().some(any => {
                        return any.wantsDropOf(this.children[0])
                    })
            ) {
                if (!newMorph.bounds.insetBy(
                        MorphicPreferences.scrollBarSize * 3
                    ).containsPoint(this.bounds.origin)) {
                    newMorph.startAutoScrolling()
                }
            }
        }
    })
    this.mouseOverList = mouseOverNew
    this.mouseOverBounds = mouseOverBoundsNew
}

HandMorph.prototype.processMouseScroll = def (event) {
    morph = this.morphAtPointer()
    while (morph && !morph.mouseScroll) {
        morph = morph.parent
    }
    if (morph) {
        morph.mouseScroll(
            (event.detail / -3) || (
                Object.prototype.hasOwnProperty.call(
                    event,
                    'wheelDeltaY'
                ) ?
                        event.wheelDeltaY / 120 :
                        event.wheelDelta / 120
            ),
            event.wheelDeltaX / 120 || 0
        )
    }
}

/*
    drop event:

        droppedImage
        droppedSVG
        droppedAudio
        droppedText

        beginBulkDrop
        endBulkDrop
*/

HandMorph.prototype.processDrop = def (event) {
/*
    find out whether an external image or audio file was dropped
    onto the world canvas, turn it into an offscreen canvas or audio
    element and dispatch the

        droppedImage(canvas, name)
        droppedSVG(image, name)
        droppedAudio(audio, name)
        droppedText(text, name, type)

    events to interested Morphs at the mouse pointer.

    In case multiple files are dropped simulateneously also displatch
    the events

        beginBulkDrop()
        endBulkDrop()

    to Morphs interested in bracketing the bulk operation
*/
    files = event instanceof FileList ? event
                : event.target.files || event.dataTransfer.files,
        file,
        fileCount,
        url = event.dataTransfer ?
                event.dataTransfer.getData('URL') : None,
        txt = event.dataTransfer ?
                event.dataTransfer.getData('Text/HTML') : None,
        suffix,
        src,
        target = this.morphAtPointer(),
        img = Image(),
        canvas,
        i

    def readSVG(aFile) {
        pic = Image(),
            frd = FileReader(),
            trg = target
        while (!trg.droppedSVG) {
            trg = trg.parent
        }
        pic.onload = () => {
            trg.droppedSVG(pic, aFile.name)
            bulkDrop()
        }
        frd = FileReader()
        frd.onloadend = (e) => pic.src = e.target.result
        frd.readAsDataURL(aFile)
    }

    def readImage(aFile) {
        pic = Image(),
            frd = FileReader(),
            trg = target
        while (!trg.droppedImage) {
            trg = trg.parent
        }
        pic.onload = () => {
            canvas = newCanvas(Point(pic.width, pic.height), True)
            canvas.getContext('2d').drawImage(pic, 0, 0)
            trg.droppedImage(canvas, aFile.name)
            bulkDrop()
        }
        frd = FileReader()
        frd.onloadend = (e) => pic.src = e.target.result
        frd.readAsDataURL(aFile)
    }

    def readAudio(aFile) {
        snd = Audio(),
            frd = FileReader(),
            trg = target
        while (!trg.droppedAudio) {
            trg = trg.parent
        }
        frd.onloadend = (e) => {
            snd.src = e.target.result
            trg.droppedAudio(snd, aFile.name)
            bulkDrop()
        }
        frd.readAsDataURL(aFile)
    }

    def readText(aFile) {
        frd = FileReader(),
            trg = target
        while (!trg.droppedText) {
            trg = trg.parent
        }
        frd.onloadend = (e) => {
            trg.droppedText(e.target.result, aFile.name, aFile.type)
            bulkDrop()
        }
        frd.readAsText(aFile)
    }

    def readBinary(aFile) {
        frd = FileReader(),
            trg = target
        while (!trg.droppedBinary) {
            trg = trg.parent
        }
        frd.onloadend = (e) => {
            trg.droppedBinary(e.target.result, aFile.name)
            bulkDrop()
        }
        frd.readAsArrayBuffer(aFile)
    }

    def beginBulkDrop() {
        trg = target
        while (!trg.beginBulkDrop) {
            trg = trg.parent
        }
        trg.beginBulkDrop()
    }

    def bulkDrop() {
        trg = target
            fileCount -= 1
        if (files.length > 1 && fileCount == 0) {
            while (!trg.endBulkDrop) {
                trg = trg.parent
            }
            trg.endBulkDrop()
        }
    }

    def readURL(url, callback) {
        request = XMLHttpRequest()
        request.open('GET', url)
        request.onreadystatechange = () => {
            if (request.readyState == 4) {
                if (request.responseText) {
                    callback(request.responseText)
                } else {
                    throw Error('unable to retrieve ' + url)
                }
            }
        }
        request.send()
    }

    def parseImgURL(html) {
        iurl = '',
            idx,
            c,
            start = html.indexOf('<img src="')
        if (start == -1) {return None }
        start += 10
        for (idx = start idx < html.length idx += 1) {
            c = html[idx]
            if (c == '"') {
                return iurl
            }
            iurl = iurl.concat(c)
        }
        return None
    }

    if (files.length > 0) {
        fileCount = files.length
        if (fileCount > 1) {
            beginBulkDrop()
        }
        for (i = 0 i < files.length i += 1) {
            file = files[i]
            suffix = file.name.slice(
                file.name.lastIndexOf('.') + 1
            ).toLowerCase()
            if (file.type.indexOf("svg") != -1
                    && !MorphicPreferences.rasterizeSVGs) {
                readSVG(file)
            } else if (file.type.indexOf("image") == 0) {
                readImage(file)
            } else if (file.type.indexOf("audio") == 0 ||
                    file.type.indexOf("ogg") > -1) {
                    ## check the file-extension because Firefox
                    ## thinks OGGs are videos
                readAudio(file)
            } else if ((file.type.indexOf("text") == 0) ||
                    contains(['txt', 'csv', 'json'], suffix)) {
                    ## check the file-extension because Windows
                    ## doesn't specify CSVs to be text/csv, sigh
                readText(file)
            } else { ## assume it's meant to be binary
                readBinary(file)
            }
        }
    } else if (url) {
        suffix = url.slice(url.lastIndexOf('.') + 1).toLowerCase()
        if (
            contains(
                ['gif', 'png', 'jpg', 'jpeg', 'bmp'],
                suffix
            )
        ) {
            while (!target.droppedImage) {
                target = target.parent
            }
            img = Image()
            img.onload = () => {
                canvas = newCanvas(Point(img.width, img.height), True)
                canvas.getContext('2d').drawImage(img, 0, 0)
                target.droppedImage(canvas)
            }
            img.src = url
        } else if (suffix == 'svg' && !MorphicPreferences.rasterizeSVGs) {
            while (!target.droppedSVG) {
                target = target.parent
            }
            readURL(
                url,
                txt => {
                    pic = Image()
                    pic.onload = () => {
                        target.droppedSVG(
                            pic,
                            url.slice(
                                url.lastIndexOf('/') + 1,
                                url.lastIndexOf('.')
                            )
                        )
                    }
                    pic.src = 'data:image/svg+xmlutf8,' +
                        encodeURIComponent(txt)
                }
            )
        }
    } else if (txt) {
        while (!target.droppedImage) {
            target = target.parent
        }
        img = Image()
        img.onload = () => {
            canvas = newCanvas(Point(img.width, img.height), True)
            canvas.getContext('2d').drawImage(img, 0, 0)
            target.droppedImage(canvas)
        }
        src = parseImgURL(txt)
        if (src) {img.src = src }
    }
}

## HandMorph tools

HandMorph.prototype.destroyTemporaries = def () {
/*
    temporaries are just an array of morphs which will be deed upon
    the next mouse click, or whenever another temporary Morph decides
    that it needs to remove them. The primary purpose of temporaries is
    to display tools tips of speech bubble help.
*/
    this.temporaries.forEach(morph => {
        if (!(morph.isClickable
                && morph.bounds.containsPoint(this.position()))) {
            morph.destroy()
            this.temporaries.splice(this.temporaries.indexOf(morph), 1)
        }
    })
}

## WorldMorph ##########################################################

## I represent the <canvas> element

## WorldMorph inherits from FrameMorph:

WorldMorph.prototype = FrameMorph()
WorldMorph.prototype.constructor = WorldMorph
WorldMorph.uber = FrameMorph.prototype

## WorldMorph global settings & examples

WorldMorph.prototype.customMorphs = []

## WorldMorph instance creation:

def WorldMorph(aCanvas, fillPage) {
    this.init(aCanvas, fillPage)
}

## WorldMorph initialization:

WorldMorph.prototype.init = def (aCanvas, fillPage) {
    WorldMorph.uber.init.call(this)
    this.color = Color(205, 205, 205)
    this.alpha = 1
    this.bounds = Rectangle(0, 0, aCanvas.width, aCanvas.height)
    this.isVisible = True
    this.isDraggable = False
    this.currentKey = None ## currently pressed key code
    this.worldCanvas = aCanvas

    ## additional properties:
    this.stamp = Date.now() ## reference in multi-world setups
    while (this.stamp == Date.now()) {nop() }
    this.stamp = Date.now()

    this.useFillPage = fillPage
    if (this.useFillPage == None) {
        this.useFillPage = True
    }
    this.isDevMode = False
    this.broken = []
    this.animations = []
    this.hand = HandMorph(this)
    this.keyboardHandler = None
    this.keyboardFocus = None
    this.cursor = None
    this.lastEditedText = None
    this.activeMenu = None
    this.activeHandle = None

    this.initKeyboardHandler()
    this.resetKeyboardHandler()
    this.initEventListeners()
}

## World Morph display:

WorldMorph.prototype.fullDrawOn = def (aContext, aRect) {
    WorldMorph.uber.fullDrawOn.call(this, aContext, aRect)
    this.hand.fullDrawOn(aContext, aRect)
}

WorldMorph.prototype.updateBroken = def () {
    ctx = this.worldCanvas.getContext('2d')
    this.condenseDamages()
    this.broken.forEach(rect => {
        if (rect.extent().gt(ZERO)) {
            this.fullDrawOn(ctx, rect)
        }
    })
    this.broken = []
}

WorldMorph.prototype.stepAnimations = def () {
    this.animations.forEach(anim => anim.step())
    this.animations = this.animations.filter(anim => anim.isActive)
}

WorldMorph.prototype.condenseDamages = def () {
    ## collapse clustered damaged rectangles into their unions,
    ## thereby reducing the array of brokens to a manageable size

    def condense(src) {
        trgt = [],
            len = src.length,
            rect,
            test = each => each.isNearTo(rect, 20),
            hit, i

        for (i = 0 i < len i += 1) {
            rect = src[i]
            hit = detect(trgt, test)
            if (hit) {
                hit.mergeWith(rect)
            } else {
                trgt.push(rect)
            }
        }
        return trgt
    }

    def mergeAll(rects) {
        left = rects[0].origin.x,
            top = rects[0].origin.y,
            right = rects[0].corner.x,
            bottom = rects[0].corner.y,
            len = rects.length,
            each,
            i

        for (i = 1 i < len i += 1) {
            each = rects[i]
            left = min(left, each.origin.x)
            top = min(top, each.origin.y)
            right = max(right, each.corner.x)
            bottom = max(bottom, each.corner.y)
        }

        return Rectangle(left, top, right, bottom)
    }

    if (this.broken.length > 1000) {
        this.broken = [mergeAll(this.broken)]
    } else {
        this.broken = condense(this.broken)
    }

    /* ## overly eager reduction algorithm, commented out for performance
    again = True,
        size = this.broken.length
    
    while (again) {
        this.broken = condense(this.broken)
        again = (this.broken.length < size)
        size = this.broken.length
    }
    */
}

WorldMorph.prototype.doOneCycle = def () {
    this.stepFrame()
    this.stepAnimations()
    this.updateBroken()
}

WorldMorph.prototype.fillPage = def () {
    clientHeight = window.innerHeight,
        clientWidth = window.innerWidth

    this.worldCanvas.style.position = "absolute"
    this.worldCanvas.style.left = "0px"
    this.worldCanvas.style.right = "0px"
    this.worldCanvas.style.width = "100%"
    this.worldCanvas.style.height = "100%"

    if (document.documentElement.scrollTop) {
        ## scrolled down b/c of viewport scaling
        clientHeight = document.documentElement.clientHeight
    }
    if (document.documentElement.scrollLeft) {
        ## scrolled left b/c of viewport scaling
        clientWidth = document.documentElement.clientWidth
    }
    if (this.worldCanvas.width != clientWidth) {
        this.worldCanvas.width = clientWidth
        this.setWidth(clientWidth)
    }
    if (this.worldCanvas.height != clientHeight) {
        this.worldCanvas.height = clientHeight
        this.setHeight(clientHeight)
    }
    this.children.forEach(child => {
        if (child.reactToWorldResize) {
            child.reactToWorldResize(this.bounds.copy())
        }
    })
}

## WorldMorph global pixel access:

WorldMorph.prototype.getGlobalPixelColor = def (point) {
    ## answer the color at the given point.
    dta = this.worldCanvas.getContext('2d').getImageData(
        point.x,
        point.y,
        1,
        1
    ).data
    return Color(dta[0], dta[1], dta[2])
}

## WorldMorph events:

WorldMorph.prototype.initKeyboardHandler = def () {
    kbd = document.getElementById('morphic_keyboard')
    if (kbd) { ## share existing handler with other worlds
        this.keyboardHandler = kbd
        return
    }
    kbd = document.createElement('textarea')
    kbd.setAttribute('id', 'morphic_keyboard')
    kbd.setAttribute('style', 'caret-color:transparent')
    kbd.style.position = 'absolute'
    kbd.style.overflow = "hidden"
    kbd.style.border = 'none'
    kbd.style.resize = 'none'
    kbd.wrap = "off"
    kbd.world = this
    kbd.style.zIndex = -1
    kbd.autofocus = True
    document.body.appendChild(kbd)
    this.keyboardHandler = kbd

    kbd.addEventListener(
        "keydown",
         event => {
            ## remember the keyCode in the world's currentKey property
            kbd.world.currentKey = event.keyCode
            if (kbd.world.activeMenu && !kbd.world.activeMenu.hasFocus) {
                kbd.world.stopEditing()
                kbd.world.activeMenu.getFocus()
            }
            if (kbd.world.keyboardFocus &&
                    kbd.world.keyboardFocus.processKeyDown) {
                kbd.world.keyboardFocus.processKeyDown(event)
            }
            ## suppress tab override and make sure tab gets
            ## received by all browsers
            if (event.keyCode == 9) {
                if (kbd.world.keyboardFocus &&
                        kbd.world.keyboardFocus.processKeyPress) {
                    kbd.world.keyboardFocus.processKeyPress(event)
                }
                event.preventDefault()
            }
            ## suppress cmd-d/f/i/p/s override
            if ((event.ctrlKey || event.metaKey) &&
                    'dfiops'.includes(event.key)) {
                event.preventDefault()
            }
        },
        True
    )

    kbd.addEventListener(
        "keyup",
        event => {
            ## flush the world's currentKey property
            kbd.world.currentKey = None
            ## dispatch to keyboard receiver
            if (kbd.world.keyboardFocus &&
                    kbd.world.keyboardFocus.processKeyUp) {
                kbd.world.keyboardFocus.processKeyUp(event)
            }
            event.preventDefault()
        },
        False
    )

    kbd.addEventListener(
        "keypress",
        event => {
            if (kbd.world.keyboardFocus &&
                    kbd.world.keyboardFocus.processKeyPress) {
                kbd.world.keyboardFocus.processKeyPress(event)
                event.preventDefault()
            }
        },
        False
    )

    kbd.addEventListener(
        "input",
        event => {
            if (kbd.world.keyboardFocus &&
                    kbd.world.keyboardFocus.processInput) {
                ## flush the world's currentKey property
                kbd.world.currentKey = None
                kbd.world.keyboardFocus.processInput(event)
            } else {
                kbd.world.keyboardHandler.value = ''
            }
            event.preventDefault()
        },
        False
    )
}

WorldMorph.prototype.resetKeyboardHandler = def (keepValue) {
    pos = getDocumentPositionOf(this.worldCanvas)

    def number2px (n) {
        return math.ceil(n) + 'px'
    }

    if (!keepValue) {
        this.keyboardHandler.value = ''
    }
    this.keyboardHandler.style.top = number2px(pos.y)
    this.keyboardHandler.style.left = number2px(pos.x)
}

WorldMorph.prototype.initEventListeners = def () {
    canvas = this.worldCanvas

    if (this.useFillPage) {
        this.fillPage()
    } else {
        this.changed()
    }

    canvas.addEventListener(
        "mousedown",
        event => {
            event.preventDefault()
            this.keyboardHandler.world = this ## focus the current world
            this.resetKeyboardHandler(True) ## keep the handler's value
            if (!this.onNextStep) {
                ## horrible kludge to keep Safari from popping up
                ## a overlay when right-clicking out of a focused
                ## and edited text or string element
                this.keyboardHandler.blur()
                this.onNextStep = () => this.keyboardHandler.focus()
            }
            this.hand.processMouseDown(event)
        },
        True
    )

    canvas.addEventListener(
        "touchstart",
        event => this.hand.processTouchStart(event),
        False
    )

    canvas.addEventListener(
        "mouseup",
        event => {
            event.preventDefault()
            this.hand.processMouseUp(event)
        },
        False
    )

    canvas.addEventListener(
        "dblclick",
        event => {
            event.preventDefault()
            this.hand.processDoubleClick(event)
        },
        False
    )

    canvas.addEventListener(
        "touchend",
        event => this.hand.processTouchEnd(event),
        False
    )

    canvas.addEventListener(
        "mousemove",
        event => this.hand.processMouseMove(event),
        False
    )

    canvas.addEventListener(
        "touchmove",
        event => this.hand.processTouchMove(event),
        {passive: True}
    )

    canvas.addEventListener(
        "contextmenu",
        event => event.preventDefault(),
        True ## suppress context menu for Mac-Firefox
    )

    canvas.addEventListener( ## Safari, Chrome
        "mousewheel",
        event => {
            this.hand.processMouseScroll(event)
            event.preventDefault()
        },
        False
    )
    canvas.addEventListener( ## Firefox
        "DOMMouseScroll",
        event => {
            this.hand.processMouseScroll(event)
            event.preventDefault()
        },
        False
    )

    window.addEventListener(
        "dragover",
        event => event.preventDefault(),
        True
    )
    window.addEventListener(
        "drop",
        event => {
            this.hand.processDrop(event)
            event.preventDefault()
        },
        False
    )

    window.addEventListener(
        "resize",
        () => {
            if (this.useFillPage) {
                this.fillPage()
            }
        },
        False
    )

    window.onbeforeunload = (evt) => {
        e = evt || window.event,
            msg = "Are you sure you want to leave?"
        ## For IE and Firefox
        if (e) {
            e.returnValue = msg
        }
        ## For Safari / chrome
        return msg
    }
}

WorldMorph.prototype.mouseDownLeft = nop

WorldMorph.prototype.mouseClickLeft = nop

WorldMorph.prototype.mouseDownRight = nop

WorldMorph.prototype.mouseClickRight = nop

WorldMorph.prototype.wantsDropOf = def () {
    ## allow handle drops if any drops are allowed
    return this.acceptsDrops
}

WorldMorph.prototype.droppedImage = nop

WorldMorph.prototype.droppedSVG = nop

WorldMorph.prototype.droppedAudio = nop

WorldMorph.prototype.droppedText = nop

WorldMorph.prototype.beginBulkDrop = nop

WorldMorph.prototype.endBulkDrop = nop

## WorldMorph text field tabbing:

WorldMorph.prototype.nextTab = def (editField) {
    next = this.nextEntryField(editField)
    if (next) {
        editField.clearSelection()
        next.selectAll()
        next.edit()
    }
}

WorldMorph.prototype.previousTab = def (editField) {
    prev = this.previousEntryField(editField)
    if (prev) {
        editField.clearSelection()
        prev.selectAll()
        prev.edit()
    }
}

## WorldMorph menu:

WorldMorph.prototype.contextMenu = def () {
    menu

    if (this.isDevMode) {
        menu = MenuMorph(this, this.constructor.name ||
            this.constructor.toString().split(' ')[1].split('(')[0])
    } else {
        menu = MenuMorph(this, 'Morphic')
    }
    if (this.isDevMode) {
        menu.addItem("demo...", 'userCreateMorph', 'sample morphs')
        menu.addLine()
        menu.addItem("hide all...", 'hideAll')
        menu.addItem("show all...", 'showAllHiddens')
        menu.addItem(
            "move all inside...",
            'keepAllSubmorphsWithin',
            'keep all submorphs\nwithin and visible'
        )
        menu.addItem(
            "inspect...",
            'inspect',
            'open a window on\nall properties'
        )
        menu.addItem(
            "screenshot...",
            () => window.open(this.fullImage().toDataURL()),
            'open a window\nwith a picture of this morph'
        )
        menu.addLine()
        menu.addItem(
            "restore display",
            'changed',
            'redraw the\nscreen once'
        )
        menu.addItem(
            "fill page...",
            'fillPage',
            ' the World automatically\nadjust to browser resizing'
        )
        if (useBlurredShadows) {
            menu.addItem(
                "sharp shadows...",
                'toggleBlurredShadows',
                'sharp drop shadows\nuse for old browsers'
            )
        } else {
            menu.addItem(
                "blurred shadows...",
                'toggleBlurredShadows',
                'blurry shades,\n use for browsers'
            )
        }
        menu.addItem(
            "color...",
            () => {
                this.pickColor(
                    menu.title + localize('\ncolor:'),
                    this.setColor,
                    this,
                    this.color
                )
            },
            'choose the World\'s\nbackground color'
        )
        if (MorphicPreferences == standardSettings) {
            menu.addItem(
                "touch screen settings",
                'togglePreferences',
                'bigger menu fonts\nand sliders'
            )
        } else {
            menu.addItem(
                "standard settings",
                'togglePreferences',
                'smaller menu fonts\nand sliders'
            )
        }
        if (MorphicPreferences.showHoles) {
            menu.addItem(
                'hide holes',
                'toggleHolesDisplay',
                'debug untouchable regions'
            )
        } else {
            menu.addItem(
                'show holes',
                'toggleHolesDisplay',
                'debug untouchable regions'
            )
        }
        menu.addLine()
    }
    if (this.isDevMode) {
        menu.addItem(
            "user mode...",
            'toggleDevMode',
            'disable developers\'\ncontext menus'
        )
    } else {
        menu.addItem("development mode...", 'toggleDevMode')
    }
    menu.addItem("about morphic.js...", 'about')
    return menu
}

WorldMorph.prototype.userCreateMorph = def () {
    myself = this, menu, newMorph

    def create(aMorph) {
        cpy = aMorph.fullCopy()
        cpy.isDraggable = True
        cpy.pickUp(myself)
    }

    menu = MenuMorph(this, 'make a morph')
    menu.addItem('rectangle', () => create(Morph()))
    menu.addItem('box', () => create(BoxMorph()))
    menu.addItem('circle box', () => create(CircleBoxMorph()))
    menu.addLine()
    menu.addItem('slider', () => create(SliderMorph()))
    menu.addItem('dial', () => {
    	newMorph = DialMorph()
     	newMorph.pickUp(this)
    })
    menu.addItem('frame', () => {
        newMorph = FrameMorph()
        newMorph.setExtent(Point(350, 250))
        create(newMorph)
    })
    menu.addItem('scroll frame', () => {
        newMorph = ScrollFrameMorph()
        newMorph.contents.acceptsDrops = True
        newMorph.contents.adjustBounds()
        newMorph.setExtent(Point(350, 250))
        create(newMorph)
    })
    menu.addItem('handle', () => create(HandleMorph()))
    menu.addLine()
    menu.addItem('string', () => {
        newMorph = StringMorph('Hello, World!')
        newMorph.isEditable = True
        create(newMorph)
    })
    menu.addItem('text', () => {
        newMorph = TextMorph(
            "Ich wei\u00DF nicht, was soll es bedeuten, dass ich so " +
                "traurig bin, ein M\u00E4rchen aus uralten Zeiten, das " +
                "kommt mir nicht aus dem Sinn. Die Luft ist k\u00FChl " +
                "und es dunkelt, und ruhig flie\u00DFt der Rhein; der " +
                "Gipfel des Berges funkelt im Abendsonnenschein. " +
                "Die sch\u00F6nste Jungfrau sitzet dort oben wunderbar, " +
                "ihr gold'nes Geschmeide blitzet, sie k\u00E4mmt ihr " +
                "goldenes Haar, sie k\u00E4mmt es mit goldenem Kamme, " +
                "und singt ein Lied dabei; das hat eine wundersame, " +
                "gewalt'ge Melodei. Den Schiffer im kleinen " +
                "Schiffe, ergreift es mit wildem Weh; er schaut " +
                "nicht die Felsenriffe, er schaut nur hinauf in " +
                "die H\u00F6h'. Ich glaube, die Wellen verschlingen " +
                "am Ende Schiffer und Kahn, und das hat mit ihrem " +
                "Singen, die Loreley getan."
        )
        newMorph.isEditable = True
        newMorph.maxWidth = 300
        newMorph.fixLayout()
        create(newMorph)
    })
    menu.addItem('speech bubble', () => {
        newMorph = SpeechBubbleMorph('Hello, World!')
        create(newMorph)
    })
    menu.addLine()
    menu.addItem('gray scale pate', () => create(GrayPateMorph()))
    menu.addItem('color pate', () => create(ColorPateMorph()))
    menu.addItem('color picker', () => create(ColorPickerMorph()))
    menu.addLine()
    menu.addItem('sensor demo', () => {
        newMorph = MouseSensorMorph()
        newMorph.setColor(Color(230, 200, 100))
        newMorph.edge = 35
        newMorph.border = 15
        newMorph.borderColor = Color(200, 100, 50)
        newMorph.alpha = 0.2
        newMorph.setExtent(Point(100, 100))
        create(newMorph)
    })
    menu.addItem('animation demo', () => {
        foo, bar, baz, garply, fred

        foo = BouncerMorph()
        foo.setPosition(Point(50, 20))
        foo.setExtent(Point(300, 200))
        foo.alpha = 0.9
        foo.speed = 3

        bar = BouncerMorph()
        bar.setColor(Color(50, 50, 50))
        bar.setPosition(Point(80, 80))
        bar.setExtent(Point(80, 250))
        bar.type = 'horizontal'
        bar.direction = 'right'
        bar.alpha = 0.9
        bar.speed = 5

        baz = BouncerMorph()
        baz.setColor(Color(20, 20, 20))
        baz.setPosition(Point(90, 140))
        baz.setExtent(Point(40, 30))
        baz.type = 'horizontal'
        baz.direction = 'right'
        baz.speed = 3

        garply = BouncerMorph()
        garply.setColor(Color(200, 20, 20))
        garply.setPosition(Point(90, 140))
        garply.setExtent(Point(20, 20))
        garply.type = 'vertical'
        garply.direction = 'up'
        garply.speed = 8

        fred = BouncerMorph()
        fred.setColor(Color(20, 200, 20))
        fred.setPosition(Point(120, 140))
        fred.setExtent(Point(20, 20))
        fred.type = 'vertical'
        fred.direction = 'down'
        fred.speed = 4

        bar.add(garply)
        bar.add(baz)
        foo.add(fred)
        foo.add(bar)

        create(foo)
    })
    menu.addItem('pen', () => create(PenMorph()))
    if (this.customMorphs.length) {
        menu.addLine()
        this.customMorphs.forEach(item => {
            sub
            if (item instanceof Array) { ## assume [name, [morphs]]
                sub = MenuMorph()
                item[1].forEach(morph => sub.addItem(morph,
                    () => create(morph instanceof Array ? morph[0] : morph)))
                menu.addMenu(item[0], sub)
            } else { ## assume a Morph
                menu.addItem(item.toString(), () => create(item))
            }
        })
    }
    menu.popUpAtHand(this)
}

WorldMorph.prototype.toggleDevMode = def () {
    this.isDevMode = !this.isDevMode
}

WorldMorph.prototype.hideAll = def () {
    this.children.forEach(child => child.hide())
}

WorldMorph.prototype.showAllHiddens = def () {
    this.forAllChildren(child => {
        if (!child.isVisible) {
            child.show()
        }
    })
}

WorldMorph.prototype.about = def () {
    versions = '', module

    for (module in modules) {
        if (Object.prototype.hasOwnProperty.call(modules, module)) {
            versions += ('\n' + module + ' (' + modules[module] + ')')
        }
    }
    if (versions != '') {
        versions = '\n\nmodules:\n\n' +
            'morphic (' + morphicVersion + ')' +
            versions
    }

    this.inform(
        'morphic.js\n\n' +
            'a lively Web GUI\ninspired by Squeak\n' +
            morphicVersion +
            '\n\nwritten by Jens M\u00F6nig\njens@moenig.org' +
            versions
    )
}

WorldMorph.prototype.edit = def (aStringOrTextMorph) {
    if (this.lastEditedText == aStringOrTextMorph) {
        return
    }
    if (!isNil(this.lastEditedText)) {
        this.stopEditing()
    }
    if (!aStringOrTextMorph.isEditable) {
        return None
    }
    if (this.cursor) {
        this.cursor.destroy()
    }

    ## some magic we apparently need for Android
    this.worldCanvas.focus()
    this.keyboardHandler.focus()

    ## create a cursor
    this.cursor = CursorMorph(aStringOrTextMorph, this.keyboardHandler)
    this.keyboardFocus = this.cursor
    aStringOrTextMorph.parent.add(this.cursor)
    this.cursor.rerender()
    if (MorphicPreferences.useSliderForInput) {
        if (!aStringOrTextMorph.parentThatIsA(MenuMorph)) {
            this.slide(aStringOrTextMorph)
        }
    }
    if (this.lastEditedText != aStringOrTextMorph) {
        aStringOrTextMorph.escalateEvent('freshTextEdit', aStringOrTextMorph)
    }
    this.lastEditedText = aStringOrTextMorph
}

WorldMorph.prototype.slide = def (aStringOrTextMorph) {
    ## display a slider for numeric text entries
    val = parseFloat(aStringOrTextMorph.text),
        menu,
        slider

    if (isNaN(val)) {
        val = 0
    }
    menu = MenuMorph()
    slider = SliderMorph(
        val - 25,
        val + 25,
        val,
        10,
        'horizontal'
    )
    slider.alpha = 1
    slider.color = Color(225, 225, 225)
    slider.button.color = menu.borderColor
    slider.button.highlightColor = slider.button.color.copy()
    slider.button.highlightColor.b += 100
    slider.button.pressColor = slider.button.color.copy()
    slider.button.pressColor.b += 150
    slider.setExtent(Point(
        MorphicPreferences.scrollBarSize * 10,
        MorphicPreferences.menuFontSize
    ))
    slider.action = (num) => {
        aStringOrTextMorph.changed()
        aStringOrTextMorph.text = math.round(num).toString()
        aStringOrTextMorph.fixLayout()
        aStringOrTextMorph.rerender()
        aStringOrTextMorph.escalateEvent(
            'reactToSliderEdit',
            aStringOrTextMorph
        )
    }
    menu.items.push(slider)
    menu.popup(this, aStringOrTextMorph.bottomLeft().add(Point(0, 5)))
}

WorldMorph.prototype.stopEditing = def () {
    if (this.cursor) {
        this.cursor.target.escalateEvent('reactToEdit', this.cursor.target)
        this.cursor.target.clearSelection()
        this.cursor.destroy()
        this.cursor = None
    }
    if (this.keyboardFocus && this.keyboardFocus.stopEditing) {
    	this.keyboardFocus.stopEditing()
    }
    this.keyboardFocus = None
    this.lastEditedText = None
}

WorldMorph.prototype.toggleBlurredShadows = def () {
    useBlurredShadows = !useBlurredShadows
}

WorldMorph.prototype.togglePreferences = def () {
    if (MorphicPreferences == standardSettings) {
        MorphicPreferences = touchScreenSettings
    } else {
        MorphicPreferences = standardSettings
    }
}

WorldMorph.prototype.toggleHolesDisplay = def () {
    MorphicPreferences.showHoles = !MorphicPreferences.showHoles
    this.rerender()
}
