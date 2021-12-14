import React from 'react';
import Chessboard from "chessboardjsx";
import $, { data } from 'jquery';
import { Button, Progress} from 'reactstrap';
import "./styles.css"

class Board extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            board: "start",
            value: 0,
        };

        this.makeHumanMove = this.makeHumanMove.bind(this);
        this.getNext = this.getNext.bind(this);
        this.reset = this.reset.bind(this);
        this.initialize = this.initialize.bind(this);
        this.getPrevious = this.getPrevious.bind(this);
    }


    componentDidMount() {
        this.setState({ board: "start",  value: 0});
        console.log("Board Mounted");
    }

    async makeHumanMove(properties) {

        const response = await fetch('/makeMove',
        {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: 'POST', 
            body: JSON.stringify(properties)
          });
        const data = await response.json();
        this.setState({board: data.board, value: data.value});
    }

    async getNext() {
        const response = await fetch('/next');
        const data = await response.json();
        this.setState({board: data.board, value: data.value});
    }

    async initialize() {
        const response = await fetch('/');
        const data = await response.json();
        return data.board
    }

    async reset() {
        const response = await fetch('/reset');
        const data = await response.json();
        this.setState({board: data.board, value: data.value})
    }
    
    async getPrevious() {
        const response = await fetch('/previous');
        const data = await response.json();
        this.setState({board: data.board, value: data.value})
    }

    renderValue() {
        var newContainer = document.getElementById("value-container");
        newContainer.innerHTML = this.state.value;
        console.log("update value");
    }
    
    render() {
        let height_value = this.state.value;
        let absolute = Math.abs(height_value);
        if (Math.abs(height_value) > 200) {
            height_value = height_value/absolute * 200
        }
        const progressbar = {
            height: 200 - this.state.value,
        };

        return (
            <div className="board" style={{ display: "flex", flexDirection: "row"}} >
                <div className="chessboard" style={{ order: 1}}>
                    <Chessboard
                    width={400}
                    position={this.state.board}
                    boardStyle={{
                        borderRadius: "5px",
                        boxShadow: `0 5px 15px rgba(0, 0, 0, 0.5)`
                      }}
                    onDrop={this.makeHumanMove}/>
                </div>

                <div className="bar" style={{order: 2, marginLeft: "410px"}}>
                    <div className="inner-bar" style={progressbar}>
                        {this.state.value}
                    </div>

                </div>

                <div className="ui" style={{ order: 3, position: "relative"}}>
                    <Button className="clicky" color='primary' onClick={this.getNext}>Next</Button>
                    <Button className="clicky" color='primary' onClick={this.getPrevious}>Previous</Button>
                    <Button className="clicky" color='danger' onClick={this.reset}>Reset</Button>
                </div>





            </div>
        );
    }

}

export default Board;