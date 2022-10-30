import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import AdbIcon from '@mui/icons-material/Adb';
import { Checkbox, List, ListItem, ListItemButton, Modal, Paper } from '@mui/material';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import NavigateBeforeIcon from '@mui/icons-material/NavigateBefore';
import SaveIcon from '@mui/icons-material/Save';
import axios from 'axios';
import SettingContext from '../context/SettingContext';
import { green, lime, yellow } from '@mui/material/colors';

function ResponsiveAppBar() {

    const context = React.useContext(SettingContext);
    const [modalopen, setModalopen] = React.useState(false);
    const [imagesdata, setImagesdata] = React.useState([]);
    const [index, setIndex] = React.useState(0)
    const [refresh, setRefresh] = React.useState(true)

    React.useEffect(() => {
        axios.get('/api/images')
            .then(res => setImagesdata(res.data))
    }, [refresh])

    React.useEffect(() => {
        console.log(imagesdata[index])
        context.updateSetting({ workingImageData: imagesdata[index], boxesData: [] })
    }, [imagesdata, index])

    const style = {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 400,
    };

    return (
        <AppBar position="static" sx={{ background: 'purple' }}>
            <Container>
                <Toolbar variant='dense'>
                    <AdbIcon sx={{ display: { xs: 'none', md: 'flex' }, mr: 1 }} />
                    <Typography
                        variant="h6"
                        noWrap
                        component="a"
                        href="/"
                        sx={{
                            mr: 2,
                            display: { xs: 'none', md: 'flex' },
                            fontFamily: 'monospace',
                            fontWeight: 700,
                            letterSpacing: '.3rem',
                            color: 'inherit',
                            textDecoration: 'none',
                        }}
                    >
                        NAFIUL
                    </Typography>

                    <Box sx={{ display: 'flex', flexGrow: 1, justifyContent: 'center', alignItems: 'center', gap: '10px' }}>
                        <Button variant="contained"
                            startIcon={<NavigateBeforeIcon />}
                            disabled={index < 1}
                            onClick={() => {
                                setIndex(old => old - 1)
                            }}
                        >
                            Prev
                        </Button>
                        <Button variant="contained" onClick={() => { setModalopen(true) }}>
                            {index + 1}/{imagesdata.length}
                        </Button>
                        <Button variant="contained"
                            endIcon={<NavigateNextIcon />}
                            disabled={index > imagesdata.length - 2}
                            onClick={() => {
                                setIndex(old => old + 1);
                            }}
                        >
                            Next
                        </Button>
                    </Box>


                    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '10px' }}>
                        {context.settings.workingImageData && context.settings.workingImageData.data !== '' && <Button
                            variant="contained"
                            endIcon={<SaveIcon />}
                            sx={{ backgroundColor: context.settings.workingImageData.data ? yellow[700] : green[500] }}
                            onClick={() => {

                                axios.post('/api/save/' + context.settings.workingImageData.file,
                                    JSON.stringify({

                                        "file": context.settings.workingImageData.file,
                                        "boxes": context.settings.boxesData

                                    }), {
                                    headers: { 'Content-Type': 'application/json' }
                                })
                                    .then(function (response) {
                                        setRefresh(old => !old)
                                        console.log(response);
                                    })
                                    .catch(function (error) {
                                        console.log(error);
                                    });
                            }}
                        >
                            {context.settings.workingImageData.data ? "ReSave" : "Save"}
                        </Button>}

                        <Button 
                            variant="contained" color="error"
                            onClick={() => {
                                axios.get('/api/delete/' + context.settings.workingImageData.file,
                                )
                                    .then(function (response) {
                                        setRefresh(old => !old)
                                        console.log(response);
                                    })
                                    .catch(function (error) {
                                        console.log(error);
                                    });
                            }}
                        >
                            RESET
                        </Button>
                    </Box>
                    <Modal
                        open={modalopen}
                        onClose={() => { setModalopen(false) }}
                        aria-labelledby="modal-modal-title"
                        aria-describedby="modal-modal-description"
                    >
                        <Box sx={style}>
                            <Paper sx={{ width: '40vw', maxHeight: '70vh' }}>
                                <List sx={{
                                    width: '100%',
                                    position: 'relative',
                                    overflow: 'auto',
                                    maxHeight: '60vh',
                                }}>
                                    {imagesdata.map((value, idx) => {
                                        return (
                                            <ListItem
                                                key={idx}
                                                disablePadding
                                            >
                                                <ListItemButton dense
                                                    selected={idx === index}
                                                    onClick={() => {
                                                        setIndex(idx)
                                                        setModalopen(false)
                                                    }}>
                                                    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
                                                        <Typography>
                                                            {value.file}
                                                        </Typography>
                                                        {/* {value.data === true ? <FavoriteIcon sx={{ color: pink[500] }} /> : <FavoriteBorderIcon />} */}
                                                        <Checkbox checked={value.data} disabled />
                                                    </Box>
                                                </ListItemButton>
                                            </ListItem>
                                        );
                                    })}
                                </List>
                            </Paper>
                        </Box>
                    </Modal>
                </Toolbar>
            </Container>
        </AppBar>
    );
}
export default ResponsiveAppBar;
