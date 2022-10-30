import axios from 'axios';
import React, { useContext, useEffect, useRef, useState } from 'react';
import { fabric } from "fabric";
import { Paper } from '@mui/material';
import { useResizeDetector } from 'react-resize-detector';
import SettingContext from '../context/SettingContext';


function Canvas() {

    const context = useContext(SettingContext)
    const canvas = useRef(null);
    const [boxlist, setBoxlist] = React.useState([])
    const [showbtn, setShowbtn] = React.useState(false)
    // const [workingMode, setWorkingMode] = React.useState(0)
    const { width, height, ref } = useResizeDetector();
    const [actualImageSize, setActualImageSize] = React.useState({ width: 1, height: 1 })


    function mouseZoom (opt) {
        var delta = opt.e.deltaY;
        var zoom = canvas.current.getZoom();
        zoom *= 0.999 ** delta;
        if (zoom > 20) zoom = 20;
        if (zoom < 0.01) zoom = 0.01;
        // canvas.current.setZoom(zoom);
        canvas.current.zoomToPoint({ x: opt.e.offsetX, y: opt.e.offsetY }, zoom);
        opt.e.preventDefault();
        opt.e.stopPropagation();
    }
    useEffect(() => {
        canvas.current = initCanvas();
        // destroy fabric on unmount

        canvas.current.on('mouse:wheel', mouseZoom)
        return () => {
            canvas.current.off('mouse:wheel', mouseZoom)
            canvas.current.dispose();
            canvas.current = null;
        };
    }, []);

    // React.useEffect(() => {
    //   console.log("Current Scale ", currentScale)
    // }, [currentScale])


    useEffect(() => {
        if (canvas.current) {
            // console.log(canvas.current.getZoom())
            // console.log(canvas.current.backgroundImage)
            if (canvas.current.backgroundImage) {
                const sx = width / canvas.current.backgroundImage.width;
                const sy = height / canvas.current.backgroundImage.height
                // console.log("Resizing Bg", width, height)
                canvas.current.backgroundImage.scaleX = sx;
                canvas.current.backgroundImage.scaleY = sy;

            }
            canvas.current.setDimensions({ width: width, height: height });
            canvas.current.renderAll();
        }
    }, [width, height])


    function downHandler({ key }) {
        if (key === 'c') {
            context.updateSetting({ workingMode: 1 })
        } else if (key === 's') {
            context.updateSetting({ workingMode: 2 })
        }
        else if (key === 'd') {
            context.updateSetting({ workingMode: 3 })
        }
    }



    useEffect(() => {


        window.addEventListener('keydown', downHandler);
        // window.addEventListener('keyup', upHandler);
        return () => {
            window.removeEventListener('keydown', downHandler);
            // window.removeEventListener('keyup', upHandler);
        };
    }, []);

    useEffect(() => {

        console.log("Working mode set to", context.settings.workingMode)

        if (context.settings.workingMode === 2) {
            const boxIds = new Set(canvas.current.getActiveObjects().map(obj => obj.id))
            const addlist = boxlist.filter(item => boxIds.has(item.id));
            console.log("Remaining List: ", addlist);
            context.updateSetting({
                boxesData: addlist,
                workingMode: 0
            })
        } else if (context.settings.workingMode === 3) {
            console.log(canvas.current.getActiveObjects());
            const boxIds = new Set(canvas.current.getActiveObjects().map(obj => obj.id))
            const addlist = boxlist.filter(item => !boxIds.has(item.id));
            canvas.current.discardActiveObject();
            context.updateSetting({
                boxesData: addlist,
                workingMode: 0
            })

        } else if (context.settings.workingMode === 1) {
            const mouseDownHandler = (options) => {
                console.log("Mouse Down Handler", options)

                canvas.current.discardActiveObject();
                var pointer = canvas.current.getPointer(options.e);
                var x = pointer.x;
                var y = pointer.y;
                console.log(x, y)

                var square = new fabric.Rect({
                    width: 10,
                    height: 10,
                    left: x,
                    top: y,
                    strokeDashArray: [2, 2],
                    strokeUniform: true,
                    stroke: 'red',
                    strokeWidth: 2,
                    fill: 'rgba(0,0,0,0)',
                    noScaleCache: false,
                });

                canvas.current.add(square);
                canvas.current.setActiveObject(square);

            }
            const mouseMoveHandler = (options) => {

                if (!canvas.current.getActiveObject()) {
                    return false;
                }
                var square = canvas.current.getActiveObject();

                var pointer = canvas.current.getPointer(options.e);
                var x = pointer.x;
                var y = pointer.y;
                var w = Math.abs(x - square.get('left')),
                    h = Math.abs(y - square.get('top'));

                if (!w || !h) {
                    return false;
                }
                square.set('width', w).set('height', h);

            }
            const mouseUpHandler = (options) => {

                if (!canvas.current.getActiveObject()) {
                    return false;
                }
                var square = canvas.current.getActiveObject();
                // canvas.current.add(square)
                const scaleX = actualImageSize.width / canvas.current.width
                const scaleY = actualImageSize.height / canvas.current.height
                context.updateSetting({
                    boxesData: [...boxlist,
                    {
                        x: square.left * scaleX,
                        y: square.top * scaleY,
                        w: square.width * scaleX,
                        h: square.height * scaleY,
                        id: Date.now()
                    }],
                    workingMode: 0
                })


            }

            if (canvas.current) {
                canvas.current.on('mouse:down', mouseDownHandler);
                canvas.current.on('mouse:move', mouseMoveHandler);
                canvas.current.on('mouse:up', mouseUpHandler);

                canvas.current.on('mouseup', () => {
                    console.log("Object up Handler")
                })

                canvas.current.on("selection:created", (options) => {
                    // console.log("Selection created",options)
                    setShowbtn(true)
                })
                canvas.current.on("selection:cleared", (options) => {
                    // console.log("Selection cleared",options)
                    setShowbtn(false)
                })

                canvas.current.on("mouse:over", (options) => {
                    // options.target.stroke='blue'
                    // options.target.dirty=true
                    // console.log("Mouse Over",options.target)
                })

                
            }

            return () => {
                if (canvas.current) {
                    canvas.current.off('mouse:down', mouseDownHandler)
                    canvas.current.off('mouse:move', mouseMoveHandler)
                    canvas.current.off('mouse:up', mouseUpHandler)
                }
            }
        }
    }, [context.settings.workingMode])

    useEffect(() => {
        if (context.settings.workingImageData && context.settings.workingImageData.file !== '') {
            fabric.Image.fromURL('/images/' + context.settings.workingImageData.file, function (img) {
                setActualImageSize({ height: img.height, width: img.width })
                canvas.current.setBackgroundImage(img, canvas.current.renderAll.bind(canvas.current), {
                    scaleX: canvas.current.width / img.width,
                    scaleY: canvas.current.height / img.height
                });
            });

            axios.get('/boxes/' + context.settings.workingImageData.file)
                .then(res => {
                    context.updateSetting({ boxesData: res.data.list })
                })
        }
        // console.log("Loading bg")
    }, [context.settings.workingImageData])

    useEffect(() => {
        setBoxlist(context.settings.boxesData)
    }, [context.settings.boxesData])

    useEffect(() => {

        function handleObjectModified(options) {
            console.log("object:modified", options)
            const target = options.target;
            const transformX = actualImageSize.width / canvas.current.width;
            const transformY = actualImageSize.height / canvas.current.height
            // console.log("Before modified", boxlist);
            const addlist = boxlist.map(item => {
                if (item.id === target.id) {
                    item.y = target.top * transformY
                    item.x = target.left * transformX
                    item.w = (target.width * target.scaleX) * transformX
                    item.h = (target.height * target.scaleY) * transformY
                    // item.scaleX=target.scaleX
                    // item.scaleY=target.scaleY
                }
                return item;
            });

            // console.log("object:modified", addlist);
            context.updateSetting({ boxesData: addlist })
        }
        if (canvas.current) {
            canvas.current.on('object:modified', handleObjectModified)
            return () => {
                canvas.current.off('object:modified', handleObjectModified)
            };
        }
    }, [boxlist])

    useEffect(() => {
        //TODO need some optimization
        console.log("Adding Bboxlist........")

        // console.log(boxlist)
        canvas.current.remove(...canvas.current.getObjects());
        // console.log("Current Index", currentScale)
        const boxIds = new Set(canvas.current.getObjects().map(obj => obj.id))
        const addlist = boxlist.filter(item => !boxIds.has(item.id)); //FIX for React strict mode double render issue.
        // console.log("add list", addlist)

        // const box_map = new Map(boxlist.map(item => [item.id, item]))
        // const canvas_object_delete = canvas.current.getObjects().filter(obj => !box_map.has(obj.id))
        // const canvas_object_add = boxlist.filter(item => !boxIds.has(item.id))

        // console.log("LOGIC",box_map,canvas_object_delete, canvas_object_add);


        // canvas.current.remove(...canvas_object_delete);
        // console.log("Fuck you width",canvas.current.width,actualImageSize.width)
        // console.log("Fuck you height",canvas.current.height,actualImageSize.height)
        const scaleX = canvas.current.width / actualImageSize.width
        const scaleY = canvas.current.height / actualImageSize.height

        addlist.forEach((val) => {
            const rect = new fabric.Rect({
                top: val.y * scaleY,
                left: val.x * scaleX,
                width: val.w,
                height: val.h,
                scaleX: scaleX,
                scaleY: scaleY,
                strokeDashArray: [1, 1],
                stroke: val.hasOwnProperty('label') ? 'green' : 'red',
                strokeWidth: 1,
                strokeUniform: true,
                fill: 'rgba(0,0,0,0)',
                id: val.id
            })
            // rect.on('mousedown', (options) => {
            //     options.target.stroke = 'blue'
            //     options.target.dirty = true
            //     console.log("mousedown", options)
            // })



            rect.on('drop', (e) => {
                // options.preventDefault();
                // var data = options.dataTransfer.getData("text");
                const val = e.e.dataTransfer.getData("drop_info")
                e.target.label = val
                const id = e.target.id;
                const addlist = boxlist.filter(item => {
                    if (item.id === id) {
                        item.label = val;
                    }
                    return item;
                });
                context.updateSetting({ boxesData: addlist })
                console.log("drop", e, addlist)
            })

            // rect.on('moving',(e)=>{
            //     console.log('moving',e)
            // })
            canvas.current.add(rect)
        })

    }, [width, height, actualImageSize.height, actualImageSize.width, boxlist])

    const initCanvas = () => (
        new fabric.Canvas('canvas', {
            height: 800,
            width: 800,
            renderOnAddRemove: true,
            centeredScaling: true
        })
    );

    return (
        <Paper sx={{ padding: '5px', maxHeight: '90vh' }} ref={ref}>
            <canvas id="canvas" />
            {/* {`${width}x${height}`} */}
        </Paper>
    );
}

export default Canvas;
