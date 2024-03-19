import "./CameraFeeds.css";

function CameraFeeds() {
  return (
    <div className="container">
      <table>
        <tr>
          <th>index</th>
          <th>Year</th>
          <th>Month</th>
          <th>Day</th>
          <th>Hour</th>
          <th>Minute</th>
          <th>Second</th>
          <th>Day of Week</th>
          <th>License Plate</th>
          <th>Vehicle Type</th>
          <th>In/Out</th>
          <th>Image Link</th>
        </tr>
        <tr>
          <td>213</td>
          <td>2024</td>
          <td>March</td>
          <td>13</td>
          <td>18</td>
          <td>30</td>
          <td>45</td>
          <td>Wednesday</td>
          <td>ABC123</td>
          <td>Car</td>
          <td>In</td>
          <td>
            <a href="https://example.com/image.jpg">Link</a>
          </td>
        </tr>
      </table>
      <div> --</div>
      <table>
        <tr>
          <th>17 - 0316</th>
          <th>127 - 0316</th>
          <th>GU - 2620</th>
          <th>wp KL -D 3248</th>
          <th>wp PI -P 3000</th>
          <th>wp AAA 3000</th>
          <th>AAA 3000</th>
        </tr>
        <tr></tr>
      </table>
    </div>
  );
}

export default CameraFeeds;
