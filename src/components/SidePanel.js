import axios from "axios";
import React, { useContext, useMemo } from "react";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Checkbox from '@mui/material/Checkbox';
import CommentIcon from '@mui/icons-material/Comment';
import { Button, Grid, Paper, Stack } from "@mui/material";
import Chip from '@mui/material/Chip';
import SettingContext from "../context/SettingContext";

export default function SidePanel(props) {
    // const { data, showBtn, onBtnClick } = props

    const context = useContext(SettingContext);
    const [boxes, setBoxes] = React.useState([])
    const [labels, setLabels] = React.useState([])

    React.useEffect(() => {
        if (context.settings.boxesData) {
            setBoxes(context.settings.boxesData)
        }
    }, [context.settings.boxesData])

    React.useEffect(() => {
        axios.get("/api/labels",)
            .then(res => setLabels(res.data))
    }, [])

    const label_remaining = useMemo(() => {
        return boxes.reduce((n, val) => n + (!val.hasOwnProperty("label")), 0);
    }, [boxes])



    return <Paper elevation={3} sx={{ padding: '2px' }}>
        <Stack>
            {/* {showBtn && <Button variant="contained" onClick={() => { onBtnClick() }}>KEEP SELECTED ONLY</Button>} */}

            <Stack
            // container
            // direction="row"
            // justifyContent="start"
            // alignItems="center"
            >

                <Grid container>
                    <Grid item xs={6}>
                        Label Count <Chip label={labels.length} variant="outlined" />
                    </Grid>
                </Grid>

                <Grid item xs={12} sx={{
                    width: '100%',
                    bgcolor: 'background.paper',
                    position: 'relative',
                    overflow: 'auto',
                    maxHeight: '50vh',
                }}>

                    {labels.map((value, index) => {
                        const labelId = `checkbox-list-label-${index}`;

                        return (
                            <Chip draggable
                                onDragStart={(e) => { 
                                    console.log(e)
                                    e.target.style.backgroundColor = 'salmon';
                                    e.dataTransfer.setData("drop_info", value); 
                                }}
                                key={index}
                                id={labelId}
                                label={value}
                                size="small"
                                variant="outlined" />
                        );
                    })}

                </Grid>
            </Stack>

            <Stack
                // container
                // direction="row"
                justifyContent="center"
                alignItems="center"
            >

                <Grid container>
                    <Grid item xs={6}>
                        Total Word: <Chip label={boxes.length} size="small" variant="outlined" />
                    </Grid>
                    <Grid item xs={6}>
                        Remaing: <Chip label={label_remaining} size="small" variant="outlined" />
                    </Grid>
                </Grid>
                <List sx={{
                    width: '100%',
                    bgcolor: 'background.paper',
                    position: 'relative',
                    overflow: 'auto',
                    maxHeight: '30vh',
                }}>
                    {boxes.map((value, index) => {
                        const labelId = `chip-${index}`
                        return (
                            <ListItem
                                key={index}
                                disablePadding
                            >
                                <ListItemButton dense >
                                    <Grid container>
                                        <Grid item xs={6}>
                                            <ListItemText id={labelId} primary={value.label ? value.label : "No label"} />
                                        </Grid>
                                        <Grid item xs={6}>
                                            <Chip label={`x: ${value.x}`} size="small" />
                                            <Chip label={`y: ${value.y}`} size="small" />

                                            <Chip label={`w: ${value.w}`} size="small" />
                                            <Chip label={`h: ${value.h}`} size="small" />
                                        </Grid>
                                    </Grid>
                                </ListItemButton>
                            </ListItem>
                        );
                    })}
                </List>
            </Stack>
        </Stack>
    </Paper>
}