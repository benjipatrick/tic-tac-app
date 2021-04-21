import React from 'react';
import ReactDOM from 'react-dom';

import './index.css'


function Square(props) {
  console.log(props.winner)
  const isButtonDisabled = props.winner != -2
  console.log(isButtonDisabled)
      return (
        <div className='box'>
            <button 
                className="button" 
                onClick={props.onClick}
                disabled={isButtonDisabled}
            >
                {props.value}
            </button>
        </div>
      );
  }
  
class Board extends React.Component {
    renderSquare(i) {
        return <Square 
        className='square'
        value={this.props.squares[i]} 
        onClick={() => this.props.onClick(i)}
        winner={this.props.winner}
        />;
    }

    render() {
        return (
            <div>
                <div className='game-board'>
                    {this.renderSquare(0)}{this.renderSquare(1)}{this.renderSquare(2)}
                    {this.renderSquare(3)}{this.renderSquare(4)}{this.renderSquare(5)}
                    {this.renderSquare(6)}{this.renderSquare(7)}{this.renderSquare(8)}
                </div>
            </div>
        );
    }
}


  
class Game extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        squares: Array(9).fill(null),
        isXTurn: true,
        winner: -2,
    };

    this.GetGameStatus = this.GetGameStatus.bind(this)
  }

  async GetGameStatus(squares) {
    console.log("Making Game Status Request")
    try {
      const response = await fetch('/game/status', {
        method:"POST",
          cache: "no-cache",
          headers:{
              "content_type":"application/json",
          },
          body:JSON.stringify(squares)
        })
      if (!response.ok) {
        throw Error(response.statusText)
      }
      const json = await response.json();
      var data = JSON.stringify(json)
      if (data == '{}') data = -2
  
      this.setState({
        winner:data,
        squares: squares,
        isXTurn: !this.state.isXTurn,  
      })
  
    } catch (error) {
      console.log(error)
    }
  }

  handleClick(i) {
    const squares = this.state.squares.slice();
    if (squares[i] != null) return
    squares[i] = this.state.isXTurn ? 'X' : 'O';
    this.GetGameStatus(squares)
    // this.setState({
    //     squares: squares,
    //     isXTurn: !this.state.isXTurn,   
    // }) 
}

  render() {
    return (
      <div className="game">
          <Board 
            squares={this.state.squares}
            onClick={(i) => this.handleClick(i)}
            winner={this.state.winner}
          />
        <div className="game-info">
          <div className="current-player">Player Turn: {this.state.isXTurn ? 'X' : 'O'}</div>
          <button className="restart-button">Reset</button>
        </div>
      </div>
    );
  }
}
  
  // ========================================
  
  ReactDOM.render(
    <Game />,
    document.getElementById('root')
  );
