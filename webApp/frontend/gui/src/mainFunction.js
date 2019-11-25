import React, { Component, Fragment } from 'react';
import { Button, TextField, Paper } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import PostList from './postList'

const style = {
    PaperLeft: { padding: 10, marginTop: 10, marginBottom: 10, height: 400, width : "100%" },
    PaperRight: { padding: 10, marginTop: 10, marginBottom: 10, height: 800, overflow : 'auto', width : "100%" },
}

class MainFunction extends Component {

    render() {
        return (
            <Fragment>
                <Grid container direction="row" style={{width : "100%"}}>
                    <Grid container direction="column" style={{width : "30%"}}>
                        <Grid item>
                            <Paper style={{ padding: 10, marginTop: 10, marginBottom: 10, height: 100 }}>
                                <TextField
                                    id="user_id"
                                    placeholder="Your ID"
                                    value={this.props.userID}
                                    variant="outlined"
                                    onChange={this.props.handleChange}
                                    margin="normal"
                                    style={{ marginTop: 10, marginRight: 5 }}
                                />
                                <Button onClick={this.props.handleSend} variant="contained" style={{ marginTop: 10 }}>
                                    Go
                                </Button>
                            </Paper>
                        </Grid>
                        <Grid item>
                            <Paper style={{ padding: 10, marginTop: 10, marginBottom: 10, height: 100 }}>User profile</Paper>
                        </Grid>
                        <Grid item>
                            <Paper style={style.PaperLeft}>Chart</Paper>
                        </Grid>
                    </Grid>
                    <Grid container style={{width : "70%"}}>
                        <Paper style={style.PaperRight} >
                            <PostList
                                posts={this.props.posts}
                            />
                        </Paper>
                    </Grid>
                </Grid>
            </Fragment>
        )
    }
}

export default MainFunction;